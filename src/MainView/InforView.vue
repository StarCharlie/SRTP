<!-- 介绍页面，希望加入左侧导航栏以及翻页功能 -->
<template>
  <el-row :gutter="20">
      <!-- 左边栏 -->
      <el-col :span="4">
        <div v-if="this.$cookies.get('menuListReady') != null && this.dataTransformOver" style="margin-top: 50px;">
            <el-input
              v-model="filterText"
              style="width: 80%; margin-left: 20px;"
              placeholder="输入关键词"
            />
            <el-tree
              :data="menuList"
              node-key="label"
              :default-expanded-keys="[this.data['mingcheng']]"
              highlight-current
              :props="defaultProps"
              accordion
              :current-node-key="this.data['mingcheng']"
              @node-click="handleNodeClick"
              :filter-node-method="filterNode"
              ref="tree"
              style="width: 80%; margin-left: 20px; margin-top: 10px"
            />
        </div>
      </el-col>

      <!-- 中间栏 -->
      <el-col :span="16">
        <!-- 这里有一个dom提前渲染的问题，为了避免则先映入v-if，等数据传输到了再显示 -->
        <div v-if="this.dataTransformOver">
          <div v-if="this.mode == 1" class="layout">
            <h1 id="title">{{ data['mingcheng'] }}</h1>
            <div style="background-color:azure"><p><strong>类别：</strong>{{ data['leibie']}}</p></div>
            <div style="background-color:beige"><p><strong>介绍：</strong>{{ data['jieshao']}}</p></div>
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
            <div style="background-color:indianred"><p><strong>类别：</strong>{{ data['leibie']}}</p></div>
            <div style="background-color:beige"><p><strong>功效：</strong>{{ data['gongxiao']}}</p></div>
            <div style="background-color:bisque"><p><strong>主治：</strong>{{ data['zhuzhi']}}</p></div>
            <div style="background-color:aquamarine"><p><strong>方例：</strong>{{ data['fangli']}}</p></div>
            <div style="background-color:blanchedalmond"><p><strong>刺灸法：</strong>{{ data['cijiufa']}}</p></div>
            <div style="background-color:goldenrod"><p><strong>其它：</strong>{{ data['qita']}}</p></div>
          </div>
          <el-button type="warning" :icon="Star" @click="like(data['id'])" style="margin-left: 100px;" round>Like</el-button>
        </div>
      </el-col>

      <!-- 右边栏 -->
      <el-col :span="4"></el-col>
  </el-row>
</template>

<script setup>
  import {Star} from '@element-plus/icons-vue'
</script>


<script>

const defaultProps = {
  children: 'children',
  label: 'label',
}

export default {
    data(){
        return {
            menuListReady: false,
            menuList: null,
            dataTransformOver: false,
            data: null,
            mode: 1,
            tags: null,
            filterText: "",
            favor: {
              category: "",
              id: "",
              user_name: "",
            },
        };
    },

    created(){
        // 如果已经有数据了，则为T
        this.menuListReady = (this.$global.search_list.length != 0)
        this.getInfor();
    },
    watch: {
      filterText(val) {
        this.$refs.tree.filter(val.trim())
      },
    },
    methods: {
        filterNode(value, data) {
          if (!value) return true
          return data.label.indexOf(value) !== -1
        },
        async getInfor(){
            this.mode = this.$route.query.category;
            this.$http.get('/home/InforView', {
              params: {
                'id': this.$route.query.id,
                'category': this.$route.query.category,
                'menuReady': (this.$cookies.get('menuListReady') != null),
              }
            }).then(res=>{
                // 首次查看左列表
                if(this.$cookies.get('menuListReady') == null){
                  var tempResult = res.data['menu'];
                  var tree = []
                  // 第一层，遍历三种名称
                  for(var key in tempResult){
                      var leibie = []
                      // 第二层，遍历类别
                      for (var leibie_key in tempResult[key]){
                        var node = []
                        for (var node_key in tempResult[key][leibie_key]){
                          node.push(
                            {
                              id: tempResult[key][leibie_key][node_key][0],
                              category: tempResult[key][leibie_key][node_key][1],
                              label: tempResult[key][leibie_key][node_key][2],
                            }
                          )
                        }
                        leibie.push(
                          {
                            label: leibie_key,
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
                  this.$cookies.set("menuListReady", true, {expires: "1D"});
                }
                this.menuList =  JSON.parse(window.sessionStorage.getItem('menuList'))
                this.data = res.data['data'][0];
                this.dataTransformOver = true;
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
        async handleNodeClick(data){
          // 只针对叶子节点
          if(data.id){
            this.mode = data.category;
              this.$http.get('/home/InforView', {
                params: {
                  'id': data.id,
                  'category': data.category,
                  'menuReady': (this.$cookies.get('menuListReady') != null),
                }
              }).then(res=>{
                this.dataTransformOver = false
                this.data = res.data['data'][0];
                this.dataTransformOver = true
              })
          }
        }
    },
}
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

/* 高光这里改 */
::v-deep
.el-tree--highlight-current
  .el-tree-node.is-current
  > .el-tree-node__content {
  /* 背景色 */
  background-color:  rgba(38, 239, 199, 0.24);
  /* 文字色 */
  color:dodgerblue;
  font-weight: bold;
}

</style>