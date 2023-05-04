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
  name: 'ImageCarousel',
  // components: {
  //   VueAwesomeSwiper
  // },
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
      printItem(item,index) {
        console.log(item);
        console.log(index)
      },
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