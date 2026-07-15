<template>
  <div class="app">
    <router-view />
    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="checked" to="/">打卡</van-tabbar-item>
      <van-tabbar-item icon="bar-chart-o" to="/stats">统计</van-tabbar-item>
      <van-tabbar-item icon="cloud-o" to="/weather">天气</van-tabbar-item>
      <van-tabbar-item icon="setting-o" to="/settings">设置</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const active = ref(0)
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: var(--bg);
  padding-bottom: 50px;
}
</style>
