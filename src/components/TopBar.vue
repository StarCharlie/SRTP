<template>
    <el-menu
      :default-active="this.$router.path"
      class="menu-1"
      mode="horizontal"
      text-color="#fff"
      :ellipsis="false"
      background-color="#2f3e4d"
      @select="handleSelect"
      router
    >
    <!-- 用户端 -->
      <div class="flex-grow" />
      <el-sub-menu index="2">
        <template #title>用户中心</template>
        <el-menu-item>
          <div v-if="this.$cookies.get('name') != null">
            <span @click="toInfor()"><strong>{{ "欢迎您：" + this.$cookies.get('name')}}</strong></span>
          </div>
          <div v-else>
            <span @click="toInfor()"><strong>登录</strong></span>
          </div>
        </el-menu-item>
        <el-menu-item>
            <div v-if="this.$cookies.get('name') != null">
              <span @click="removeCookie()"><strong>注销</strong></span>
            </div>
            <div v-else>
              <span @click="removeCookie()"><strong>注册</strong></span>
            </div>
        </el-menu-item>
      </el-sub-menu>
    </el-menu>

    <div style="background:#EDEBEB;">
      <el-row :gutter="20">
          <!-- 图片部分 -->
          <el-col :span="3">
            <div style="height: 90px;">
              <img src="../assets/logo.png" class="image" >
            </div>
          </el-col>
          <el-col :span="21">
            <div style="line-height: 60px;">
              <h2 style="text-align: left;">中医艾灸可视化知识服务平台</h2>
            </div>
          </el-col>
        </el-row>
    </div>

    <el-menu
      :default-active="activeIndex2"
      class="menu-2"
      mode="horizontal"
      background-color="#90C2C3"
      text-color="#fff"
      active-text-color="#ffd04b"
      popper-effect="light"
      @select="handleSelect"
      router
    >
      <el-menu-item index="/"> 主页 </el-menu-item>
      <el-menu-item index="/search"> 关键词搜索 </el-menu-item>
      <el-menu-item index="/compare"> 知识图谱 </el-menu-item>
      <el-menu-item index="/statistics"> 3D人体查看 </el-menu-item>
    </el-menu>
  </template>

  <script>
  import { watch } from 'vue'
  import router from '../router/index.js'
    watch(
        () => router.currentRoute.value['name'],
        (oldValue, newValue) => {
          if(oldValue == "mainHome" && newValue == "login"){
            router.go(0);
          }
        }
    );
  export default {
      data(){
        return{
            enter_user: (this.$cookies.get('name') != null) ? true:false
        }
      },
      methods: {
        // 登录/进入用户界面
        toInfor(){
          if(this.$cookies.get('name') == null) this.$router.push("/login");
          else this.$router.push("/main");
        },
        // 注册/注销
        removeCookie(){
          if(this.$cookies.get('name') == null) this.$router.push("/register");
          else{
            this.$cookies.remove("name");
            this.$router.go(0);
          }
        },
      }
    }
</script>



<style scoped>
  .menu-1 > {
    color: #789;
  }

  .image{
    height: 90px; 
    width: 90px;
    margin-left: 40px;
  }
  .flex-grow {
    flex-grow: 1;
  }
  </style>
  
