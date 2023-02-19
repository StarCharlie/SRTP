<!-- 侧边栏 -->
<template>
  <div style="background-color: aliceblue;">
    <el-container style="height: 700px;">
      <el-aside width="200px">
        <el-menu default-active = "1-1"
        background-color = aliceblue
        >
          <el-menu-item-group>
            <router-link class="alink" to="/graph">
              <el-menu-item index="1-1"> 知识图谱 </el-menu-item>
            </router-link>
            <router-link class="alink" to="/graph/QA">
              <el-menu-item index="1-2"> AI医生 </el-menu-item>
            </router-link>
            <router-link class="alink" to="/graph/config">
              <el-menu-item index="1-3"> 设置 </el-menu-item>
            </router-link>
          </el-menu-item-group>
        </el-menu>
      </el-aside>
      <div style="width: 100%;">
        <router-view></router-view>
      </div>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "MySpace",
  data() {
    return {};
  },
};
</script>

<style scoped>

.el-aside {
  color: #333;
}
.router-link-active {
  text-decoration: none;
}

.alink {
  text-decoration: none;
}
</style>
