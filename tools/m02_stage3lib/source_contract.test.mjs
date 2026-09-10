import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import path from 'node:path'
import test from 'node:test'
import { fileURLToPath } from 'node:url'
import { isInside } from './harness.mjs'

const here = path.dirname(fileURLToPath(import.meta.url))
const harnessPath = path.join(here, 'harness.mjs')

test('harness has no direct WAS import or listener call', async () => {
  const source = await fs.readFile(harnessPath, 'utf8')
  assert.doesNotMatch(source, /from\s+['"]was-teaching-server['"]/)
  assert.doesNotMatch(source, /\.listen\s*\(/)
  assert.match(source, /import\(['"]was-teaching-server['"]\)/)
})

test('network guards precede dynamic WAS import', async () => {
  const source = await fs.readFile(harnessPath, 'utf8')
  const guard = source.indexOf('restoreGuards = installNetworkGuards(events)')
  const importWAS = source.indexOf("import('was-teaching-server')")
  assert.ok(guard >= 0)
  assert.ok(importWAS > guard)
})

test('bounded configuration and unconditional cleanup remain explicit', async () => {
  const source = await fs.readFile(harnessPath, 'utf8')
  for (const required of [
    'capacityBytes',
    'maxUploadBytes',
    'maxSpacesPerController',
    'maxCollectionsPerSpace',
    'maxResourcesPerSpace',
    'finally',
    'fs.rm(PACKAGE_LINK',
    'fs.rm(MODULES_DIR',
    'fs.rm(dataRoot'
  ]) {
    assert.match(source, new RegExp(required.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')))
  }
})

test('repository boundary predicate distinguishes inside and outside paths', () => {
  assert.equal(isInside('/repo/tools/data', '/repo'), true)
  assert.equal(isInside('/repo', '/repo'), true)
  assert.equal(isInside('/private/tmp/data', '/repo'), false)
})

test('both finite deadlines and fail-closed marker expiry are explicit', async () => {
  const source = await fs.readFile(harnessPath, 'utf8')
  assert.match(source, /OBSERVATION_TIMEOUT_MS = 15_000/)
  assert.match(source, /OVERALL_TIMEOUT_MS = 60_000/)
  assert.match(source, /throw new Error\('PREIMPORT_OBSERVATION_TIMEOUT'\)/)
  assert.match(source, /process\.exitCode = 124/)
})
