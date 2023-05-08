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
  <div style="height:100%; background-color:#D2DEDC">
    <el-row :gutter="20">
      <el-col :span="3"></el-col>
      <el-col :span="9">
        <div class="radius" >
          <el-scrollbar style="height: 350px; width:100%">
            <div class="block" style="height: 100%">
              <div style="height:50px;text-align: center">
                <el-row class="mb-4" style="margin-left: 42%; margin-top: 1%">
                  <h3>十四经络穴</h3>
                </el-row>
              </div>
              <el-carousel style="overflow: hidden;">
                <el-carousel-item v-for="(item, index) in gallery" :key="index">
                  <img :src="item.src" style="width:550px; height:250px; margin-top:1%; margin:auto; display: flex;justify-content: center;align-items: center;" >
                </el-carousel-item>
              </el-carousel>
            </div>
          </el-scrollbar>
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
              <p style="margin-left: 20px;" @click="toInfor(this.mode, item['id'])">{{ item['id'] + '. ' + item['mingcheng'] }}</p>
            </div>
          </el-scrollbar>
        </div>
      </el-col>
      <el-col :span="3"></el-col>
    </el-row>
    <!-- 页面列表展开展示 -->
    <div v-if="this.dataTransformOver" style="margin-top: 50px; width: 100%;">
      <div style=" width: 80%;  margin: auto">
        <div v-for="item in this.menuList" :key="item.label">
          <!-- 一级标签 -->
          <div style="text-align: center; background-color: gray; padding: 5px; margin: 20px">{{item.label}}</div>
          <div v-for="subItem in item.children" :key="subItem.label" style="width: 100%;">
            <!-- 二级标签 -->
            <div style="margin: 5px;">
              <el-row :gutter="20">
                <el-col :span="4">
                  <div style="text-align:center; background-color:bisque; margin: 5px; padding: 5px;">{{ subItem.label }}</div>
                </el-col>
                <el-col :span="20">
                  <!-- 三级标签 -->
                  <div class="tag-group" v-for="node in subItem.children" :key="node.label">
                    <el-tag class="ml-2"
                            :type="node.category === 1 ? 'info' : (node.category === 2 ? 'warning' : 'success')"
                            @click="toInfor(node.category, node.id)">{{node.label}}</el-tag>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <el-divider>
    <el-icon><star-filled /></el-icon>
  </el-divider>
  <div class="centered">
    <p class="project-info">数据来源:上海市中医药文献馆,网址http://www.pharmnet.com.cn/tcm/jf/</p>
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
.tag-group {
  display: inline-block;
  vertical-align: top;
  margin: 5px;
}

.centered {
    margin: auto;
    height: 30px;
    text-align: center;
  }
  .project-info {
    font-size: 8px;
    color: #999;
  }
  .title-info{
    font-size: 10px;
    color:dimgray;
  }

</style>

<script>

export const strcut = (str) => {
      if(str.length >= 200) str = str.substring(0, 200) + "...";
      return str;
    }
export default {
  name: 'ImageCarousel',
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
            dataTransformOver: false,
            menuList: null,
          gallery:[
            {src: require('/src/assets/ImgRoll/resize/任脉穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/督脉穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/手厥阴心包经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/手太阳小肠经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/手太阴肺经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/手少阳三焦经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/手少阴心经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/手阳明大肠经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/足厥阴肝经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/足太阳膀胱经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/足太阴脾经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/足少阳胆经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/足少阴肾经穴.jpg')},
            {src: require('@/assets/ImgRoll/resize/足阳明胃经穴.jpg')},

          ]
        };
    },

    created(){
        this.getData(1);
    },

    methods: {
        async getData(mode){
          this.mode = mode
          this.$http.get('/home/HomeView', {
            params: {
              'mode': this.mode,
              'menuReady': (window.sessionStorage.getItem('menuList') != null),
            }
          }).then(res=>{
              this.data = res.data['data'];
              if(window.sessionStorage.getItem('menuList') == null){
                var tempResult = res.data['menu'];
                var tree = []
                // 第一层，遍历三种名称
                for(var key in tempResult){
                    var leibie = []
                    // 第二层，遍历类别
                    for (var leibie_key in tempResult[key]){
                      var node = []
                      for (var node_key in tempResult[key][leibie_key][1]){
                        node.push(
                          {
                            id: tempResult[key][leibie_key][1][node_key][0],
                            category: tempResult[key][leibie_key][1][node_key][1],
                            label: tempResult[key][leibie_key][1][node_key][2],
                          }
                        )
                      }
                      leibie.push(
                        {
                          label: tempResult[key][leibie_key][0],
                          children: node
                        }
                      )
                    }
                    tree.push(
                      { 
                        label: key,
                        children: leibie
                      }
                    )
                }
                window.sessionStorage.setItem("menuList", JSON.stringify(tree))
              }
              this.menuList = JSON.parse(window.sessionStorage.getItem('menuList'));
              this.dataTransformOver = true;
          });
        },
        async toInfor(category, id){
          this.$router.push({
            path: '/Infor',
            query: {
              category: category,
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
        },
    },
}

</script>


<script setup>
  import {Search} from '@element-plus/icons-vue'
  import { StarFilled } from '@element-plus/icons-vue'
</script>