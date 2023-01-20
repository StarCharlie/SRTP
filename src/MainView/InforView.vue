<template>
  <div style="margin: auto; width: 80%;">
    <div v-if="this.mode == 1" class="layout">
      <h1 id="title">{{ data['mingcheng'] }}</h1>
      <div style="background-color:azure">
        <p><strong>介绍：</strong>{{ data['jieshao']}}</p>
      </div>
    </div>
    <div v-else-if="this.mode == 2" class="layout">
      <h1 id="title">{{ data['mingcheng'] }}</h1>
      <div style="background-color:azure"><p><strong>类别：</strong>{{ data['leibie']}}</p></div>
      <div style="background-color:beige"><p><strong>症状：</strong>{{ data['bingzheng']}}</p></div>
      <div style="background-color:bisque"><p><strong>治疗：</strong>{{ data['zhiliao']}}</p></div>
    </div>
    <div v-else class="layout">
      <h1 id="title">{{ data['mingcheng'] }}</h1>
      <div style="background-color:azure"><p><strong>位置：</strong>{{ data['weizhi']}}</p></div>
      <div style="background-color:beige"><p><strong>功效：</strong>{{ data['gongxiao']}}</p></div>
      <div style="background-color:bisque"><p><strong>主治：</strong>{{ data['zhuzhi']}}</p></div>
      <div style="background-color:aquamarine"><p><strong>方例：</strong>{{ data['fangli']}}</p></div>
      <div style="background-color:blanchedalmond"><p><strong>刺灸法：</strong>{{ data['cijiufa']}}</p></div>
      <div style="background-color:goldenrod"><p><strong>其它：</strong>{{ data['qita']}}</p></div>
    </div>
    <el-button type="warning" :icon="Star" @click="like(data['id'])" style="margin-left: 100px;" round>Like</el-button>
  </div>
</template>

<script>
export default {
    inject: ['reload'],
    data(){
        return {
            data: null,
            linkData: null,
            mode: 1,
            tags: null,
            favor: {
              category: "",
              id: "",
              user_name: "",
            },
        };
    },

    created(){
        this.getInfor();
    },
    methods: {
        async getInfor(){
          this.mode = this.$route.query.category;
            this.$http.get('/home/InforView', {
              params: {
                'id': this.$route.query.id,
                'category': this.$route.query.category
              }
            }).then(res=>{
                this.data = res.data['data'][0];
            });
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
  import {Star} from '@element-plus/icons-vue'
</script>

<style scoped>
.layout {
  position: static;
  margin: 5% 5% 2%;
  background: #fff;
  text-align: left;
  line-height: 30px;
}
.relatedpaper{
  position: static;
  float: left;
  margin: 0px;
  padding: 5%;
  background: #fff;
}
.paper {
  position: static;
  margin: 20px 0px;
  width: auto;
  background: #fff;
  text-align: left;
  line-height: 20px;
}
h2 {
    text-align: left;
    padding-left: 10px;
}
.paperdate {
    font-size: x-small;
}
.paperabstract {
    font-size: smaller;
}
.tag {
    margin: 0px 10px;
}
body {
  margin: 0px;
  padding: 0;
}
#date, #author {
    font-size: small;
    color: grey;
}
</style>