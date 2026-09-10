import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import dgram from 'node:dgram'
import fs from 'node:fs/promises'
import net from 'node:net'
import os from 'node:os'
import path from 'node:path'
import tls from 'node:tls'
import { fileURLToPath } from 'node:url'

const EXPECTED_CHECKOUT =
  '/private/tmp/m02-stage3lib-20260910/was-teaching-server'
const EXPECTED_COMMIT = '2090a606f2723e4d57ef0090db55fd1bdab9427e'
const SERVER_URL = 'http://127.0.0.1:46321'
const READY_MARKER = 'M02_STAGE3LIB_PREIMPORT_READY'
const COMPLETION_FILE =
  '/private/tmp/m02-stage3lib-20260910/observer.complete'
const OBSERVATION_TIMEOUT_MS = 15_000
const OVERALL_TIMEOUT_MS = 60_000
const HERE = path.dirname(fileURLToPath(import.meta.url))
const SOGA_ROOT = path.resolve(HERE, '..', '..')
const MODULES_DIR = path.join(HERE, 'node_modules')
const PACKAGE_LINK = path.join(MODULES_DIR, 'was-teaching-server')

function safeShape(args) {
  const first = args[0]
  if (typeof first === 'number') {
    return { kind: 'network', port: first, hostType: typeof args[1] }
  }
  if (typeof first === 'string') return { kind: 'ipc', valueLength: first.length }
  if (first && typeof first === 'object') {
    return {
      kind: 'options',
      hasPort: Object.hasOwn(first, 'port'),
      hasHost: Object.hasOwn(first, 'host'),
      hasPath: Object.hasOwn(first, 'path')
    }
  }
  return { kind: 'unknown', argumentType: typeof first }
}

function installNetworkGuards(events) {
  const originals = {
    listen: net.Server.prototype.listen,
    connect: net.Socket.prototype.connect,
    tlsConnect: tls.connect,
    createSocket: dgram.createSocket,
    bind: dgram.Socket.prototype.bind,
    fetch: globalThis.fetch
  }
  const reject = (entry) => {
    events.push(entry)
    throw new Error(`PROHIBITED_NETWORK_ATTEMPT:${entry.api}`)
  }
  net.Server.prototype.listen = function (...args) {
    return reject({ api: 'net.Server.listen', ...safeShape(args) })
  }
  net.Socket.prototype.connect = function (...args) {
    return reject({ api: 'net.Socket.connect', ...safeShape(args) })
  }
  tls.connect = function (...args) {
    return reject({ api: 'tls.connect', ...safeShape(args) })
  }
  dgram.createSocket = function (...args) {
    return reject({ api: 'dgram.createSocket', ...safeShape(args) })
  }
  dgram.Socket.prototype.bind = function (...args) {
    return reject({ api: 'dgram.Socket.bind', ...safeShape(args) })
  }
  if (typeof originals.fetch === 'function') {
    globalThis.fetch = async function (...args) {
      const first = args[0]
      events.push({ api: 'fetch', inputType: typeof first })
      throw new Error('PROHIBITED_NETWORK_ATTEMPT:fetch')
    }
  }
  return () => {
    net.Server.prototype.listen = originals.listen
    net.Socket.prototype.connect = originals.connect
    tls.connect = originals.tlsConnect
    dgram.createSocket = originals.createSocket
    dgram.Socket.prototype.bind = originals.bind
    if (originals.fetch === undefined) delete globalThis.fetch
    else globalThis.fetch = originals.fetch
  }
}

async function waitForObserver() {
  process.stdout.write(`${READY_MARKER}\n`)
  const deadline = Date.now() + OBSERVATION_TIMEOUT_MS
  while (Date.now() < deadline) {
    try {
      await fs.access(COMPLETION_FILE)
      return
    } catch (error) {
      if (error?.code !== 'ENOENT') throw error
    }
    await new Promise((resolve) => setTimeout(resolve, 100))
  }
  throw new Error('PREIMPORT_OBSERVATION_TIMEOUT')
}

export function isInside(candidate, parent) {
  const relative = path.relative(parent, candidate)
  return (
    relative === '' ||
    (!path.isAbsolute(relative) && relative !== '..' && !relative.startsWith(`..${path.sep}`))
  )
}

async function assertExactCheckout() {
  const head = (await fs.readFile(path.join(EXPECTED_CHECKOUT, '.git', 'HEAD'), 'utf8')).trim()
  assert.equal(head, EXPECTED_COMMIT, 'preserved checkout HEAD changed')
}

function emit(record) {
  process.stdout.write(`${JSON.stringify(record)}\n`)
}

function redactedMessage(error, secrets) {
  let message = typeof error?.message === 'string' ? error.message : 'HARNESS_FAILURE'
  for (const secret of secrets) {
    if (secret) message = message.split(secret).join('[REDACTED]')
  }
  return message
}

function assertNotAborted(signal) {
  if (signal.aborted) throw signal.reason ?? new Error('OVERALL_TIMEOUT')
}

function withAbort(promise, signal) {
  if (signal.aborted) return Promise.reject(signal.reason)
  return new Promise((resolve, reject) => {
    const onAbort = () => reject(signal.reason)
    signal.addEventListener('abort', onAbort, { once: true })
    Promise.resolve(promise).then(
      (value) => {
        signal.removeEventListener('abort', onAbort)
        resolve(value)
      },
      (error) => {
        signal.removeEventListener('abort', onAbort)
        reject(error)
      }
    )
  })
}

export async function run() {
  const events = []
  let app
  let dataRoot
  let restoreGuards
  let moduleTreeCreated = false
  let timedOut = false
  let primaryError
  const secrets = []
  const abortController = new AbortController()
  let watchdog
  watchdog = setTimeout(() => {
    timedOut = true
    abortController.abort(new Error('OVERALL_TIMEOUT'))
  }, OVERALL_TIMEOUT_MS)

  try {
    const signal = abortController.signal
        await assertExactCheckout()
        assertNotAborted(signal)
        await fs.access(path.join(SOGA_ROOT, '.git'))
        await fs.rm(COMPLETION_FILE, { force: true })
        assertNotAborted(signal)
        dataRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'm02-stage3lib-data-'))
        const realData = await fs.realpath(dataRoot)
        const realSoga = await fs.realpath(SOGA_ROOT)
        const realCheckout = await fs.realpath(EXPECTED_CHECKOUT)
        assert.ok(!isInside(realData, realSoga), 'data root is inside SOGA')
        assert.ok(
          !isInside(realData, realCheckout),
          'data root is inside WAS checkout'
        )

        restoreGuards = installNetworkGuards(events)
        await waitForObserver()
        assertNotAborted(signal)
        await fs.mkdir(MODULES_DIR, { recursive: false })
        moduleTreeCreated = true
        await fs.symlink(EXPECTED_CHECKOUT, PACKAGE_LINK, 'dir')
        assertNotAborted(signal)

        const { createApp, FileSystemBackend } = await withAbort(
          import('was-teaching-server'),
          signal
        )
        assertNotAborted(signal)
        const backend = new FileSystemBackend({
          dataDir: dataRoot,
          capacityBytes: 1_048_576,
          maxUploadBytes: 65_536,
          maxSpacesPerController: 2,
          maxCollectionsPerSpace: 4,
          maxResourcesPerSpace: 8
        })
        const onboardingToken = crypto.randomBytes(32).toString('base64url')
        secrets.push(onboardingToken)
        const { publicKey } = crypto.generateKeyPairSync('ed25519')
        const spki = publicKey.export({ type: 'spki', format: 'der' })
        const controller = `did:key:z${base58btc(Buffer.concat([Buffer.from([0xed, 0x01]), spki.subarray(-32)]))}`
        secrets.push(controller)
        app = createApp({ backend, onboardingToken, serverUrl: SERVER_URL })

        const health = await withAbort(
          app.inject({ method: 'GET', url: '/health' }),
          signal
        )
        assertNotAborted(signal)
        emit({
          event: 'health',
          requestClass: 'non_mutating',
          status: health.statusCode,
          contentType: health.headers['content-type'] ?? null
        })
        assert.equal(health.statusCode, 200)

        const spaceId = `stage3lib-${crypto.randomUUID()}`
        const created = await withAbort(
          app.inject({
            method: 'POST',
            url: '/spaces/',
            headers: {
              authorization: `Bearer ${onboardingToken}`,
              'content-type': 'application/json'
            },
            payload: { id: spaceId, name: 'Stage 3-Lib temporary space', controller }
          }),
          signal
        )
        assertNotAborted(signal)
        const stored = await withAbort(backend.getSpaceDescription({ spaceId }), signal)
        assertNotAborted(signal)
        emit({
          event: 'space_provision',
          requestClass: 'bounded_temporary_write',
          status: created.statusCode,
          hasLocation: typeof created.headers.location === 'string',
          stored: stored?.id === spaceId,
          transition: 'absent_to_present'
        })
        assert.equal(created.statusCode, 201)
        assert.equal(stored?.id, spaceId)

        emit({
          event: 'resource_and_precondition_scope',
          status: 'skipped',
          reason: 'no resource exists; creating one requires zcap verification not supplied by this phase'
        })
        assert.deepEqual(events, [], 'network-attempt guard recorded an event')
        emit({
          event: 'complete',
          physicalOutcome: 'not_applicable',
          networkAttempts: events.length
        })
  } catch (error) {
    primaryError = new Error(redactedMessage(error, secrets))
    throw primaryError
  } finally {
    clearTimeout(watchdog)
    const cleanupErrors = []
    const settle = async (label, operation) => {
      try {
        await operation()
      } catch (error) {
        cleanupErrors.push({ label, error: redactedMessage(error, secrets) })
      }
    }
    if (app) await settle('app_close', () => app.close())
    if (restoreGuards) await settle('guard_restore', async () => restoreGuards())
    if (moduleTreeCreated) {
      await settle('package_link_remove', () => fs.rm(PACKAGE_LINK, { force: true }))
      await settle('module_tree_remove', () => fs.rm(MODULES_DIR, { recursive: true, force: true }))
    }
    if (dataRoot) await settle('data_root_remove', () => fs.rm(dataRoot, { recursive: true, force: true }))
    await settle('completion_marker_remove', () => fs.rm(COMPLETION_FILE, { force: true }))
    emit({ event: 'cleanup', ok: cleanupErrors.length === 0, errors: cleanupErrors })
    if (cleanupErrors.length > 0) {
      const cleanupFailure = new AggregateError(
        cleanupErrors.map((entry) => new Error(`${entry.label}: ${entry.error}`)),
        'CLEANUP_FAILURE'
      )
      if (primaryError) primaryError.cause = cleanupFailure
      else throw cleanupFailure
    }
    if (timedOut) process.exitCode = 124
  }
}

function base58btc(bytes) {
  const alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
  let value = 0n
  for (const byte of bytes) value = value * 256n + BigInt(byte)
  let encoded = ''
  while (value > 0n) {
    encoded = alphabet[Number(value % 58n)] + encoded
    value /= 58n
  }
  for (const byte of bytes) {
    if (byte !== 0) break
    encoded = `1${encoded}`
  }
  return encoded
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  run().catch((error) => {
    process.stderr.write(`${redactedMessage(error, [])}\n`)
    if (process.exitCode !== 124) process.exitCode = 1
  })
}
