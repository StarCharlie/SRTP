<template>
    <body id="poster">
      <div
        class="layout"
        style="margin-left: 40px; box-shadow: 12px 12px 12px rgba(0, 0, 0, 0.1)"
      >
        <h1 style="text-align:center">Login</h1>
        <el-form
          label-position="right"
          label-width="60px"
          style="max-width: 460px"
          class="loginForm"
        >
          <el-form-item label="账号：">
            <el-input v-model="loginForm.username" />
          </el-form-item>
          <el-form-item label="密码：">
            <el-input type="password" v-model="loginForm.password" />
          </el-form-item>
          <el-row class="loginBtn">
            <el-button
              plain
              type="primary"
              class="loginBtn"
              @click="login"
              style="width: 48%; margin-bottom: 15px"
              color="#90C2C3"
              text-color="#fff"
              >登录
            </el-button>
            <el-button
              plain
              type="primary"
              class="registerBtn"
              @click="register"
              style="width: 48%; margin-bottom: 15px"
              color="#90C2C3"
              text-color="#fff"
              >注册
            </el-button>
          </el-row>
        </el-form>
      </div>
    </body>
  </template>
  
  <script>
  export default {
    data(){
      return{
        loginForm: {
          username: "",
          password: ""
        },
        rules: {
          rName: [
            { required: true, message: '请输入姓名', trigger: 'blur' },
          ],
          rPassword:[
            { required: true, message: '请输入金额', trigger: 'blur' },     
          ],
        }
      }
    },

    methods: {
      login(){
        this.$http.post('/LoginView',this.loginForm).then(red=>{
          if(red.data['message'] == "success"){
            this.$cookies.set("name", this.loginForm['username'], {expires: "1D"});
            this.$router.push("/");
          }
          else{
            alert(red.data['message']);
          }
        });
      },
      register(){
        this.$router.push("/Register")
      }
    }
  }
  </script>
  
  <style scoped>
  .layout {
    position: absolute;
    top: 25%;
    left: calc(50% - 250px);
    border-radius: 15px;
    background-clip: padding-box;
    margin: 90px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }
  
  #poster {
    /* background: url("../pictures/login.jpg") no-repeat;
    background-position: center; */
    height: 100%;
    width: 100%;
    background-size: cover;
    background-color: #f5feff;
    position: absolute;
  }
  body {
    margin: 0px;
    padding: 0;
  }
  </style>
  