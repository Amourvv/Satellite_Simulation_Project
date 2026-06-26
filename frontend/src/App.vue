<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Scenario } from './types/scenario'

const scenario = ref<Scenario | null>(null)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/scenario')
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`)
    }
    scenario.value = await response.json()
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unknown request error'
  }
})
</script>

<template>
  <main class="app-shell">
    <section class="viewer">
      <div class="viewer-placeholder">
        <p>Cesium Viewer</p>
        <span>卫星、轨道、地面站和可见链路将在这里显示</span>
      </div>
    </section>

    <aside class="side-panel">
      <header>
        <p>Satellite Resource Platform</p>
        <h1>多层卫星网络资源管理仿真</h1>
      </header>

      <div v-if="error" class="status error">{{ error }}</div>
      <div v-else-if="!scenario" class="status">加载场景中...</div>
      <template v-else>
        <section>
          <h2>场景</h2>
          <p>{{ scenario.name }}</p>
          <small>{{ scenario.epoch_iso }}</small>
        </section>

        <section>
          <h2>节点</h2>
          <ul>
            <li v-for="satellite in scenario.satellites" :key="satellite.id">
              <strong>{{ satellite.name }}</strong>
              <span>{{ satellite.layer }} · {{ satellite.orbit_altitude_km }} km</span>
            </li>
          </ul>
        </section>

        <section>
          <h2>链路</h2>
          <ul>
            <li v-for="link in scenario.links" :key="link.id">
              <strong>{{ link.source_id }} -> {{ link.target_id }}</strong>
              <span>
                {{ link.visible ? 'visible' : 'blocked' }} ·
                {{ link.elevation_deg }} deg ·
                {{ link.capacity_mbps }} Mbps
              </span>
            </li>
          </ul>
        </section>
      </template>
    </aside>
  </main>
</template>

