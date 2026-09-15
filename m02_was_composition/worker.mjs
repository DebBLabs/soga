import assert from 'node:assert/strict'
import childProcess from 'node:child_process'
import crypto from 'node:crypto'
import dgram from 'node:dgram'
import dns from 'node:dns'
import dnsPromises from 'node:dns/promises'
import fs from 'node:fs/promises'
import net from 'node:net'
import path from 'node:path'
import tls from 'node:tls'
import workerThreads from 'node:worker_threads'
import { Readable } from 'node:stream'
import { createRequire, syncBuiltinESMExports } from 'node:module'
import { pathToFileURL } from 'node:url'

const MAX_INPUT = 65536
const MAX_READBACK = 32768
const SAFE_INTEGER = Number.MAX_SAFE_INTEGER
const ID = /^[A-Za-z0-9._~-]+$/
const RESERVED_COLLECTION = new Set(['backends','collections','export','import','linkset','policy','query','quotas'])
const RESERVED_RESOURCE = new Set(['backend','linkset','meta','policy','query','quota'])
const guardEvents = []

function fail(stage, detail) { throw new Error(`${stage}:${detail}`) }

function validate(value, where = '$') {
  if (value === null || typeof value === 'boolean') return
  if (typeof value === 'number') {
    if (!Number.isSafeInteger(value) || Object.is(value, -0)) fail('canonicalization', where)
    return
  }
  if (typeof value === 'string') {
    if (!/^[\x00-\x7f]*$/.test(value)) fail('canonicalization', where)
    return
  }
  if (Array.isArray(value)) return value.forEach((item, index) => validate(item, `${where}[${index}]`))
  if (!value || Object.getPrototypeOf(value) !== Object.prototype) fail('canonicalization', where)
  for (const [key, item] of Object.entries(value)) {
    if (!/^[\x00-\x7f]*$/.test(key)) fail('canonicalization', where)
    validate(item, `${where}.${key}`)
  }
}

function ordered(value) {
  if (Array.isArray(value)) return value.map(ordered)
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])]))
  }
  return value
}

function canonical(value) {
  validate(value)
  return Buffer.from(JSON.stringify(ordered(value)), 'utf8')
}

function canonicalSelfTest() {
  const fixtures = [{ z: true, a: 1 }, { v: '\b\f\n\r\t\x00\x1f\x7f' }, { min: -SAFE_INTEGER, max: SAFE_INTEGER }]
  let rejectedNegativeZero = false
  try { canonical({ v: -0 }) } catch { rejectedNegativeZero = true }
  if (!rejectedNegativeZero) fail('canonicalization', 'negative_zero')
  return fixtures.map(value => crypto.createHash('sha256').update(canonical(value)).digest('hex'))
}

function base58btc(bytes) {
  const alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
  let number = BigInt(`0x${Buffer.from(bytes).toString('hex')}`)
  let encoded = ''
  while (number > 0n) {
    encoded = alphabet[Number(number % 58n)] + encoded
    number /= 58n
  }
  for (const byte of bytes) { if (byte === 0) encoded = `1${encoded}`; else break }
  return encoded
}

function validId(value, reserved = new Set()) {
  return typeof value === 'string' && value !== '.' && value !== '..' && ID.test(value) && !reserved.has(value)
}

function installGuards(events) {
  const reject = api => (..._args) => { events.push(api); fail('prohibited_api', api) }
  const rejectConstructor = api => function (..._args) { events.push(api); fail('prohibited_api', api) }
  net.Server.prototype.listen = reject('net.listen')
  net.Socket.prototype.connect = reject('net.connect')
  tls.connect = reject('tls.connect')
  dgram.createSocket = reject('dgram.createSocket')
  dgram.Socket.prototype.bind = reject('dgram.bind')
  globalThis.fetch = reject('fetch')
  for (const name of ['spawn','exec','execFile','fork']) childProcess[name] = reject(`child_process.${name}`)
  dns.lookup = reject('dns.lookup')
  dns.resolve = reject('dns.resolve')
  dnsPromises.lookup = reject('dns.promises.lookup')
  dnsPromises.resolve = reject('dns.promises.resolve')
  workerThreads.Worker = rejectConstructor('worker_threads.Worker')
  syncBuiltinESMExports()
}

async function readAll(stream) {
  const parts = []
  let total = 0
  for await (const chunk of stream) {
    total += chunk.length
    if (total > MAX_READBACK) fail('readback', 'too_large')
    parts.push(Buffer.from(chunk))
  }
  return Buffer.concat(parts)
}

async function writeAndRead(backend, ids, envelope) {
  const bytes = canonical(envelope)
  let idempotent = false
  let version
  try {
    ({ version } = await backend.writeResource({
      ...ids,
      input: { kind: 'binary', contentType: 'application/json', stream: Readable.from(bytes), declaredBytes: bytes.length },
      ifNoneMatch: true
    }))
  } catch (error) {
    if (error?.constructor?.name !== 'PreconditionFailedError') throw error
    idempotent = true
  }
  const result = await backend.getResource(ids)
  const stored = await readAll(result.resourceStream)
  if (result.storedResourceType !== 'application/json') fail('readback', 'content_type')
  if (!stored.equals(bytes)) fail(idempotent ? 'collision' : 'readback', 'bytes')
  if (!canonical(JSON.parse(stored)).equals(bytes)) fail('readback', 'canonical')
  if (!Number.isSafeInteger(result.version) || (!idempotent && result.version !== version)) fail('readback', 'version')
  return { idempotent, version: version ?? result.version, s256: crypto.createHash('sha256').update(stored).digest('hex') }
}

async function main() {
  const chunks = []
  let size = 0
  for await (const chunk of process.stdin) {
    size += chunk.length
    if (size > MAX_INPUT) fail('input', 'too_large')
    chunks.push(chunk)
  }
  const request = JSON.parse(Buffer.concat(chunks).toString('utf8'))
  assert.deepEqual(canonical(request), Buffer.concat(chunks))
  if (!['store', 'duplicate', 'collision', 'guard_child', 'guard_dns', 'guard_network', 'guard_worker', 'guard_spawn', 'guard_exec'].includes(request.mode)) fail('mode', 'unsupported')
  if (request.envelope?.interpretation !== 'person_server_evidence_only') fail('binding', 'interpretation')
  if (request.mode !== 'store' && request.secondEnvelope?.request_id !== request.envelope?.request_id) fail('binding', 'second_request')
  const events = guardEvents
  installGuards(events)
  if (request.mode === 'guard_dns') await dnsPromises.lookup(null)
  if (request.mode === 'guard_network') net.connect({ port: -1 })
  if (request.mode === 'guard_worker') new workerThreads.Worker('')
  if (request.mode === 'guard_spawn') childProcess.spawn('')
  if (request.mode === 'guard_exec') childProcess.exec('')
  const packageRoot = await fs.realpath(request.packageRoot)
  const dataRoot = await fs.realpath(request.dataRoot)
  if (!dataRoot.startsWith('/private/tmp/m02-stage3b-run-') || packageRoot.startsWith(dataRoot) || dataRoot.startsWith(packageRoot)) fail('boundary', 'data_root')
  if ((await fs.readdir(dataRoot)).length !== 0) fail('boundary', 'data_not_empty')
  await fs.writeFile(request.readyPath, 'ready\n', { flag: 'wx' })
  const releaseDeadline = Date.now() + 10_000
  while (Date.now() < releaseDeadline) {
    try { await fs.access(request.releasePath); break } catch (error) { if (error?.code !== 'ENOENT') throw error }
    await new Promise(resolve => setTimeout(resolve, 20))
  }
  try { await fs.access(request.releasePath) } catch { fail('holdpoint', 'not_released') }
  const linkRoot = request.moduleRoot
  if (!linkRoot.startsWith('/private/tmp/m02-stage3b-run-')) fail('boundary', 'module_root')
  await fs.mkdir(linkRoot)
  const modules = path.join(linkRoot, 'node_modules')
  await fs.mkdir(modules)
  await fs.symlink(packageRoot, path.join(modules, 'was-teaching-server'), 'dir')
  try {
    const resolver = createRequire(path.join(linkRoot, 'resolver.cjs'))
    const entry = resolver.resolve('was-teaching-server')
    assert.equal(await fs.realpath(entry), path.join(packageRoot, 'dist', 'index.js'))
    const { FileSystemBackend } = await import(pathToFileURL(entry).href)
    const backendOptions = { dataDir: dataRoot, maxUploadBytes: MAX_READBACK, maxSpacesPerController: 1, maxCollectionsPerSpace: 1, maxResourcesPerSpace: 1 }
    if (request.mode === 'guard_child') backendOptions.capacityBytes = 1
    const backend = new FileSystemBackend(backendOptions)
    const ids = { spaceId: 'soga-stage3b', collectionId: 'person-server-evidence', resourceId: request.envelope.request_id }
    if (!validId(ids.spaceId) || !validId(ids.collectionId, RESERVED_COLLECTION) || !validId(ids.resourceId, RESERVED_RESOURCE)) fail('identifier', 'invalid')
    const testDidKey = `did:key:z${base58btc(Buffer.concat([Buffer.from([0xed, 0x01]), crypto.randomBytes(32)]))}`
    await backend.writeSpace({ spaceId: ids.spaceId, spaceDescription: { id: ids.spaceId, type: ['Space'], controller: testDidKey } })
    await backend.writeCollection({ spaceId: ids.spaceId, collectionId: ids.collectionId, collectionDescription: { id: ids.collectionId, type: ['Collection'] } })
    const first = await writeAndRead(backend, ids, request.envelope)
    let second = null
    if (request.mode === 'duplicate' || request.mode === 'collision') second = await writeAndRead(backend, ids, request.secondEnvelope)
    assert.deepEqual(events, [])
    process.stdout.write(JSON.stringify({ ok: true, first, second, canonicalFixtures: canonicalSelfTest(), networkAttempts: events.length }))
  } finally {
    await fs.rm(linkRoot, { recursive: true, force: true })
  }
}

main().catch(error => {
  const guarded = guardEvents.length > 0
  const stage = guarded ? 'prohibited_api' : String(error?.message ?? 'worker_failure').split(':', 1)[0]
  process.stderr.write(JSON.stringify({ ok: false, stage, guard: guarded ? guardEvents.at(-1) : null }))
  process.exitCode = 1
})
