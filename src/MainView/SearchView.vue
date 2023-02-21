<!-- for search -->
<template>
    <el-row :gutter="20">
      <el-col :span="16" :offset="4">
        <el-input v-model="transform.word" placeholder="请搜索">
            <template #append>
                <el-button style="margin-left: -20px; margin-top: 0px; height: 60px;width: 70px; font-size: 40px;" @click="search" :icon="Search" round/>
            </template>
        </el-input>
      </el-col>
      <el-col :span="4"></el-col>
    </el-row>
    <el-row :gutter="20" v-if="showResult">
        <el-col :span="20" :offset="2">
            <!-- 对card进行相关的设计 -->
              <el-card v-for="item in data" :key="item" shadow="always">
                <el-row :gutter="20">
                  <!-- 图片部分 -->
                  <el-col :span="5">
                    <img src="../assets/logo.png" class="image">
                  </el-col>
                  <!-- 文字部分 -->
                  <el-col :span="13" :offset="1">
                    <h2 id="title" v-html="item['mingcheng']"></h2>
                    <p id="weizhi" v-html="item['weizhi']"></p>
                  </el-col>
                  <!-- 按钮部分 -->
                  <el-col :span="5">
                    <div style="text-align: -webkit-center">
                      <el-button type="primary" style="width:150px" @click="toInfor(item['id'])">详情</el-button>
                    </div>
                  </el-col>
                </el-row>
              </el-card>
              <div style="vertical-align: middle;text-align:center; margin-top: 50px; margin-left: 100px">
                <el-pagination
                  class="page"
                  background
                  layout="prev, pager, next"
                  :total="200"
                  @current-change="pageswitch()"
                  v-model:current-page="currentPage"
                />
              </div>
        </el-col>
        <el-col :span="2"></el-col>
    </el-row>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>

<script>
    export const highLight = (str, key) => {
        if(key == "") return str;
        if(str.length >= 200) str = str.substring(0, 200) + "...";
        const reg = new RegExp(key, 'ig')
        return str.replace(reg, (val) => {
            return `<span style="color:#66CCFF">${val}</span>`
        })
    }
    export default {
    data(){
        return{
        transform: {
            word: ""
        },
        data: null,
        showResult: false,
        favor: {
            id: "",
            user_name: "",
          },
        }
    },
    created(){
      if(this.$route.query.word != null){
        this.transform.word = this.$route.query.word
      }
      this.search();
    },
    methods: {
        cSuggestions(suggestions){
            suggestions.map(item => {
                item['mingcheng'] = highLight(item['mingcheng'], this.transform.word)
                item['weizhi'] = highLight(item['weizhi'], this.transform.word)
            })
            this.data = suggestions;
        },
        search(){
            this.$http.post('/home/search', this.transform).then(res=>{
                this.showResult = true;
                this.cSuggestions(res.data['data']);
            });
        },
        async toInfor(id){
          this.$router.push({
            path: '/Infor',
            query: {
              id: id
            }
          })
        },
        async toLink(link){
          window.open(link, '_blank')
        },
        async like(id){
            this.favor['user_name'] = (this.$cookies.get('name') == null) ? -1 : this.$cookies.get('name');
            this.favor['id'] = id;
            this.$http.post('/HomeView', this.favor).then(res=>{
              if(res.data['message'] == "success") alert("收藏成功");
              else alert(res.data['message']);
            });
        },
    }
  }
  </script>

<style scoped>

.el-button{
  margin-left: 10px;
  margin-top: 20px;
}

.el-card{
  margin-top: 50px;
}
.image{
  margin-top: 40px;
  height: 150px; 
  width: 250px;
}
.el-input{
    margin-top: 30px;
    height: 60px;
}
</style>