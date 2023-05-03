<template>
  <div style="width: 100%;height: 120px;">
      <div style="line-height: 120px;text-align: center;margin:auto;">
        <el-row :gutter="20">
          <el-col :span="16" :offset="4">
            <el-input v-model="transform.word" placeholder="请输入查询关键词">
                <template #append>
                    <el-button style="margin-left: -20px; margin-top: 0px; height: 60px;width: 70px; font-size: 40px;" @click="search" :icon="Search" round/>
                </template>
            </el-input>
          </el-col>
          <el-col :span="4"></el-col>
        </el-row>
      </div>
  </div>
  <div style="height:500px; background-color:#D2DEDC">
    <el-row :gutter="20">
      <el-col :span="3"></el-col>
      <el-col :span="9">
        <div class="radius" style="margin-right: 10px;">
        </div>
      </el-col>
      <el-col :span="9">
        <div class="radius" style="margin-left: 10px;">
          <!-- 选择按钮 -->
          <div style="height:50px;text-align: center">
            <el-row class="mb-4" style="margin-left: 30%;">
              <el-button type="primary" @click="getData(1)">灸法</el-button>
              <el-button type="success" @click="getData(2)">病症</el-button>
              <el-button type="warning" @click="getData(3)">穴位</el-button>
            </el-row>
          </div>
          <el-scrollbar style="height: 250px; margin: 20px;">
            <div v-for="item in this.data" :key="item" class="scrollbar-demo-item">
              <p style="margin-left: 20px;" @click="toInfor(item['id'])">{{ item['mingcheng'] }}</p>
            </div>
          </el-scrollbar>
        </div>
      </el-col>
      <el-col :span="3"></el-col>
    </el-row>
  </div>

</template>

<style scoped>
#date, #author {
    font-size: small;
    color: grey;
}
.el-button{
  margin-left: 10px;
  margin-top: 20px;
}
.image{
  margin-top: 40px;
  height: 150px; 
  width: 250px;
}
.el-card{
  margin-bottom: 50px;
}
.radius {
  height: 350px;
  background-color: #ECF6F5;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 50px;
}
.scrollbar-demo-item {
  display: flex;
  height: 50px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  background: #FFF;
  color: black;
}
</style>

<script>
export const strcut = (str) => {
      if(str.length >= 200) str = str.substring(0, 200) + "...";
      return str;
    }
export default {
    data(){
        return {
            transform: {
              word: ""
            },
            mode: 1,
            data: null,
            favor: {
              category: "",
              id: "",
              user_name: "",
            },
        };
    },

    created(){
        this.getData(1);
    },

    methods: {
        async getData(mode){
          this.mode = mode
          this.$http.get('/home/HomeView', {
            params: {'mode': this.mode}
          }).then(res=>{
              this.data = res.data['data'];
          });
        },

        async toInfor(id){
          this.$router.push({
            path: '/Infor',
            query: {
              category: this.mode,
              id: id,
            }
          })
        },

        async search(){
          this.$router.push({
            path: '/search',
            query: {
              word: this.transform.word
            }
          })
        },

        async like(category, id){
            this.favor['user_name'] = (this.$cookies.get('name') == null) ? -1 : this.$cookies.get('name');
            this.favor['category'] = category;
            this.favor['id'] = id;
            this.$http.post('/home/HomeView', this.favor).then(res=>{
              if(res.data['message'] == "success") alert("收藏成功");
              else alert(res.data['message']);
            });
        }
    },
}
</script>


<script setup>
  import {Search} from '@element-plus/icons-vue'
</script>