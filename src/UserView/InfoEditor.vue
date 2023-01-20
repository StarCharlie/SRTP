<template>
  <div style="width: 70%; margin-top: 5%">
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-dynamic"
    >
      <el-form-item
        style="width: 49%"
        label="用户名"
        prop="new_name"
        :rules="[
          {
            required: true,
            message: '请注意用户名长度在3~15个字符',
            trigger: 'blur',
          },
          { min: 3, max: 15, message: '长度在 3 到 5 个字符', trigger: 'blur' },
        ]"
      >
        <el-input v-model="ruleForm.new_name"></el-input>
      </el-form-item>
      <br />
      <el-form-item label="性别" prop="region">
        <el-select v-model="sex" placeholder="请选择性别">
          <el-option label="男" value="shanghai"></el-option>
          <el-option label="女" value="beijing"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item
        style="width: 49%"
        label="城市"
        prop="city"
        :rules="[
          {
            required: false,
            message: '请注意长度在2~20个字符',
            trigger: 'blur',
          },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' },
        ]"
      >
        <el-input v-model="ruleForm.city"></el-input>
      </el-form-item>

      <el-form-item
        style="width: 60%"
        prop="email"
        label="邮箱"
        :rules="[
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          {
            type: 'email',
            message: '请输入正确的邮箱地址',
            trigger: ['blur', 'change'],
          },
        ]"
      >
        <el-input v-model="ruleForm.email"></el-input>
      </el-form-item>

      <el-form-item
        style="width: 80%; height: 120px"
        label="座右铭"
        prop="motto"
        :rules="[
          { required: false, message: '请输入座右铭', trigger: 'blur' },
          {
            min: 0,
            max: 150,
            message: '请注意长度不能超过150个字符',
            trigger: 'blur',
          },
        ]"
      >
        <el-input
          type="textarea"
          style="height: 100px; resize: none"
          v-model="ruleForm.motto"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button
          plain
          type="primary"
          @click="submitForm('ruleForm')"
          color="#90C2C3"
          >提交修改</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "InfoEditor",
  data() {
    return {
      ruleForm: {
        old_name: "",
        new_name: "",
        email: "",
        city: "",
        motto: "",
      },
      sex: "",
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ruleForm.old_name = this.$cookies.get('name')
          this.$http.post('/UserView', this.ruleForm).then(res=>{
              if(res.data['message'] == "success"){
                alert("修改成功");
                this.$cookies.set('name', this.ruleForm.new_name, {expires: "1D"}) 
                this.$router.go(0);
              }
              else alert(res.data['message']);
            });
        } else {
          return false;
        }
      });
    },
  },
};
</script>

<style scoped></style>
