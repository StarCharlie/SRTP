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
            <!-- 选择框 -->
            <div style="text-align: center;">
                <el-checkbox v-model="transform.select_infor.xuewei" @change="search()" label="穴位" size="large" />
                <el-checkbox v-model="transform.select_infor.jiufa" @change="search()" label="灸法" size="large" />
                <el-checkbox v-model="transform.select_infor.bingzheng" @change="search()" label="病症" size="large" />
            </div>
            <!-- 对card进行相关的设计 -->
              <el-card v-for="item in data" :key="item" shadow="always">
                <el-row :gutter="20">
                  <!-- 图片部分 -->
                  <el-col :span="5">
                    <img src="../assets/logo.png" class="image">
                  </el-col>
                  <!-- 文字部分 -->
                  <el-col :span="13" :offset="1">
                    <h2 id="title" v-html="item['title']"></h2>
                    <!-- 总有一天我会把这个逆天操作改掉 -->
                    <el-tag class="ml-2" size="large" :type="index_translate(item['index'])[1]" >{{ index_translate(item['index'])[0] }}</el-tag>
                    <p id="infor" v-html="item['infor']"></p>
                  </el-col>
                  <!-- 按钮部分 -->
                  <el-col :span="5">
                    <div style="text-align: -webkit-center">
                      <el-button type="primary" style="width:150px" @click="toInfor(item['id'],  index_translate(item['index'])[2])">详情</el-button>
                    </div>
                  </el-col>
                </el-row>
              </el-card>
              <div style="margin-top: 50px; margin-left: 20px; margin-bottom: 50px;">
                <el-pagination
                  @size-change="search()"
                  @current-change="search()"
                  v-model:current-page="transform.page_number"
                  :page-sizes="[5, 10, 15, 20]"
                  v-model:page-size="transform.page_size"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="totalNumber">
                </el-pagination>
              </div>
        </el-col>
        <el-col :span="2"></el-col>
    </el-row>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>

<script>
    const highLight = (str, key) => {
        if(key == "") return str;
        if(str.length >= 200) str = str.substring(0, 200) + "...";
        const reg = new RegExp(key, 'ig')
        return str.replace(reg, (val) => {
            return `<span style="color:#66CCFF">${val}</span>`
        })

    }
    const index_translate = (name) =>{
      if(name == "xuewei_infor") return ["穴位", "success", 0]
      else if(name == "jiufa_infor") return ["灸法", "info", 1]
      else if(name == "bingzheng_infor") return ["病症", "warning", 2]
      else return "其它"
    }


    export default {
    data(){
        return{
        transform: {
            word: "",
            page_number: 1,
            page_size: 10,
            select_infor: {
                xuewei: true,
                jiufa: true,
                bingzheng: true,
            },
        },
        data: null,
        totalNumber: null,
        showResult: false,
        favor: {
              infor_category: "",
              user_id: "",
              infor_id: "",
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
                item['title'] = highLight(item['title'], this.transform.word)
                item['infor'] = highLight(item['infor'], this.transform.word)
            })
            this.data = suggestions;
        },
        search(){
            this.$http.post('/home/search', this.transform).then(res=>{
                this.showResult = true;
                this.cSuggestions(res.data['data']);
                this.totalNumber = res.data['totalNumber'];
            });
        },
        async toInfor(id, category){
          this.$router.push({
            path: '/Infor',
            query: {
              'id': id,
              'category': category,
            }
          })
        },
        async like(id){
            this.favor['user_id'] = (this.$cookies.get('id') == null) ? -1 : this.$cookies.get('id');
            this.favor['infor_category'] = this.$route.query.category;
            this.favor['infor_id'] = id;
            this.$http.post('/home/HomeView', this.favor).then(res=>{
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