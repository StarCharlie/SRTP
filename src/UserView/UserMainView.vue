<template>
  <div>
    <el-container style="height: 600px; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: white">
        <el-menu default-active = "1-1">
          <el-submenu index="1">
            <el-menu-item-group>
              <router-link class="alink" to="/main/">
                <el-menu-item index="1-1"> 基本信息 </el-menu-item>
              </router-link>

              <router-link class="alink" to="/main/infoeditor">
                <el-menu-item index="1-2"> 资料修改 </el-menu-item>
              </router-link>

              <router-link class="alink" to="/main/accounteditor">
                <el-menu-item index="1-3"> 账户管理 </el-menu-item>
              </router-link>
            </el-menu-item-group>
          </el-submenu>

          <el-submenu index="2">
            <template v-slot:title>
              <i class="el-icon-postcard"></i>论文管理</template
            >
            <el-menu-item-group>
              <router-link class="alink" to="/main/myarticle">
                <el-menu-item index="2-1"> 论文收藏 </el-menu-item>
              </router-link>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container
        style="
          background-image: url(/static/logo/noticesbg.jpg);
          background-repeat: no-repeat;
          background-size: 100% 100%;
        "
      >
        <el-main>
          <div style="width: 80%; margin: 0 auto">
            <router-view></router-view>
          </div>
        </el-main>
      </el-container>
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
.el-header {
  background-color: #e5efe2;
  color: #333;
  line-height: 60px;
}

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
