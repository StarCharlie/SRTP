<template>
  <TopBar />
  <router-view></router-view>
  <el-backtop :right="100" :bottom="100" />
</template>

<script>
import TopBar from "./components/TopBar.vue";
export default {
  name: "MyApp",
  components: {
    TopBar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>