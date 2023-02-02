<template>
  <body id="poster">
    <div
      class="layout"
      style="margin-left: 40px; box-shadow: 12px 12px 12px rgba(0, 0, 0, 0.1)"
    >
      <h1 style="text-align: center">Register</h1>
      <el-form
        :model="registerForm"
        :rules="rules"
        ref="registerForm"
        label-width="100px"
        class="demo-dynamic"
      >
        <el-form-item 
        prop="user_name" 
        label="用户名"
        :rules="[
          {
            required: true,
            message: '请注意用户名长度在3~15个字符',
            trigger: 'blur',
          },
          { min: 3, max: 15, message: '长度在 3 到 5 个字符', trigger: 'blur' },
        ]">
          <el-input v-model="registerForm.user_name"></el-input>
        </el-form-item>
        
        <el-form-item 
        prop="email" 
        label="邮箱："
        :rules="[
          {
            required: true,
            message: '邮箱不能为空',
            trigger: 'blur',
          },
          {
            pattern: /^([a-zA-Z]|[0-9])(\w)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/,
            message: '请输入合法的邮箱',
            trigger: 'blur',
          },
        ]">
          <el-input v-model="registerForm.email" />
        </el-form-item>
        <el-form-item prop="password" label="密码："
        :rules="[
          {
            required: true,
            message: '密码不能为空',
            trigger: 'blur',
          },
          {
            pattern:
              /^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$)([^\u4e00-\u9fa5\s]){6,20}$/,
            message:
              '请输入6-20位英文字母,数字或者符号 且至少包含两种',
            trigger: 'blur',
          },
        ]">
        <el-input type="password" v-model="registerForm.password" />
        </el-form-item>
        <el-form-item prop="confirmPassword" label="确认密码："
        :rules="[
          {
            required: true,
            message: '密码不能为空',
            trigger: 'blur',
          },
          {
            pattern:
              /^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$)([^\u4e00-\u9fa5\s]){6,20}$/,
            message:
              '请输入6-20位英文字母,数字或者符号 且至少包含两种',
            trigger: 'blur',
          },
        ]">
          <el-input
            type="password"
            v-model="registerForm.confirmPassword"
            @blur="confirmFunc"
          />
        </el-form-item>
        <el-row>
          <el-checkbox
            class="checkBox"
            v-model="registerForm.rAgree"
            label="同意用户使用准则"
            name="type"
          />
        </el-row>
        <el-button
          v-if="registerForm.rAgree"
          type="primary"
          style="width: 96%; margin-bottom: 15px"
          class="loginBtn"
          @click="register"
          color="#90C2C3"
          text-color="#fff"
        >
          注册
        </el-button>
      </el-form>
    </div>
  </body>
</template>

<script>
import { ElMessage } from "element-plus";
export default {
  data() {
    return {
      registerForm: {
        user_name: "",
        email: "",
        password: "",
        confirmPassword: "",
        identifyCode: "",
        rAgree: 0,
      },
    };
  },

  methods: {
    register() {
      this.$refs.registerForm.validate((valid) => {
        if (!valid) {
          this.message("warning", "请修改正确的数据格式！");
          return;
        } else {
          this.$http.post("/user/RegisterView", this.registerForm).then((red) => {
            if (red.data["message"] == "success") {
              this.$router.push("/login");
            } else {
              alert(red.data["message"]);
            }
          });
        }
      });
    },
    confirmFunc() {
      if (this.registerForm.confirmPassword !== this.registerForm.password)
        ElMessage.error("密码与确认密码不一致.");
    },
  },
};
</script>

<style scoped>
.layout {
  position: absolute;
  top: 15%;
  left: calc(50% - 300px);
  border-radius: 15px;
  background-clip: padding-box;
  margin: 90px auto;
  width: 450px;
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
