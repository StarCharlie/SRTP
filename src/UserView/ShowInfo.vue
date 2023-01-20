<template>
  <div>
    <div
      style="width: 14%;height: 130px;border-radius: 100px;display: inline-block;"
    >
      <img
        style="width: 100%; height: 100%; border-radius: 100px"
        src="@/assets/default-profile.png"
        class="image"
      />
    </div>

    <br />
    <br />
    <el-descriptions :column="1">
      <el-descriptions-item label="用户名" v-model="user_name"
        ><p class="message">{{ data.user_name }}</p></el-descriptions-item
      >
      <el-descriptions-item label="邮箱号" v-model="email" class="message"
        ><p class="message">{{ data.email }}</p></el-descriptions-item
      >
      <el-descriptions-item label="座右铭" v-model="motto" class="message"
        ><p class="message">{{ data.motto }}</p></el-descriptions-item
      >
      <el-descriptions-item label="居住地" v-model="city" class="message"
        ><p class="message">{{ data.city }}</p></el-descriptions-item
      >
    </el-descriptions>
  </div>
</template>

<script>
export default {
  name: "ShowInfo",
  data() {
    return {
      data:{
        "user_name": "",
        "email": "",
        "motto": "",
        "city": "",
      }
    };
  },
  created(){
      this.getInfor();
  },
  methods: {
      async getInfor(){
          this.$http.get('/UserView', {
              params: {'user_name': this.$cookies.get('name')}
            }).then(res=>{
              this.data = res.data['data'];
            });
      },
  },
};
</script>

<style scoped>
.message {
  width: 30em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-left: 20px;
  color:dodgerblue;
}
</style>
