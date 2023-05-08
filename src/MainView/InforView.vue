<!-- 介绍页面，希望加入左侧导航栏以及翻页功能 -->
<template>
  <el-row :gutter="20">
      <!-- 左边栏 -->
      <el-col :span="4">
        <div v-if="this.dataTransformOver" style="margin-top: 50px;">
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
      <el-col :span="15">
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
            <div v-if="this.data['gongxiao']" style="background-color:beige"><p><strong>功效：</strong>{{ data['gongxiao']}}</p></div>
            <div style="background-color:bisque"><p><strong>主治：</strong>{{ data['zhuzhi']}}</p></div>
            <div v-if="this.data['fangli']" style="background-color:aquamarine"><p><strong>方例：</strong>{{ data['fangli']}}</p></div>
            <div style="background-color:blanchedalmond"><p><strong>刺灸法：</strong>{{ data['cijiufa']}}</p></div>
            <!-- <div style="background-color:goldenrod"><p><strong>其它：</strong>{{ data['qita']}}</p></div> -->
          </div>
          <el-button type="warning" :icon="Star" @click="like(data['id'])" style="margin-left: 100px;" round>Like</el-button>
        </div>

        <el-divider>
          <el-icon><star-filled /></el-icon>
        </el-divider>
        <div style="height:800px; width: 90%; margin: auto">
          <GraphInfor ref="igraph"></GraphInfor>
        </div>
        <el-divider>
          <el-icon><star-filled /></el-icon>
        </el-divider>
        <div class="centered">
          <p class="title-info">--数据来源--</p>
          <p class="project-info">详情信息：上海市中医药文献馆,网址http://www.pharmnet.com.cn/tcm/jf/</p>
          <p class="project-info">关系抽取：《实用常见病艾灸疗法》、《零基础学中医艾灸》、《艾灸穴位新解》、《简易针灸治疗法(艾灸篇)》</p>
        </div>
      </el-col>

      <!-- 右边栏 -->
      <el-col :span="5">
        <el-card class="box-card" style="margin-top: 20px; margin-right: 20px;">
          <template #header>
            <div class="card-header">
              <span>相关链接</span>
            </div>
          </template>
          <div>
            <div>
              <p>病症</p>
              <div class="tag-group" v-for='item in relationList.bingzheng' :key="item[1]">
                <el-tag class="ml-2" type="warning" @click="tagClick(item[0], 2)">{{item[1]}}</el-tag>
              </div>
            </div>
            <div>
              <p>灸法</p>
              <div class="tag-group" v-for='item in relationList.jiufa' :key="item[1]">
                <el-tag class="ml-2" type="info" @click="tagClick(item[0], 1)">{{item[1]}}</el-tag>
              </div>
            </div>
            <div>
              <p>穴位</p>
              <div class="tag-group"  v-for='item in relationList.xuewei' :key="item[1]">
                <el-tag class="ml-2" type="success" @click="tagClick(item[0], 3)">{{item[1]}}</el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
  </el-row>
</template>

<script setup>
  import {Star} from '@element-plus/icons-vue'
  import { StarFilled } from '@element-plus/icons-vue'
</script>


<script>

const defaultProps = {
  children: 'children',
  label: 'label',
}
import GraphInfor from "../GraphView/GraphInfor.vue"
export default {
    name: "GraphInfor",
    components:{
      GraphInfor,
    },
    data(){
        return {
            menuListReady: false,
            menuList: null,
            dataTransformOver: false,
            relationList: {
              bingzheng: "",
              xuewei: "",
              jiufa: "",
            },
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
              }
            }).then(res=>{
                this.menuList =  JSON.parse(window.sessionStorage.getItem('menuList'))
                this.data = res.data['data'][0];
                this.relationList.xuewei = res.data['relation'].xuewei;
                this.relationList.bingzheng = res.data['relation'].bingzheng;
                this.relationList.jiufa = res.data['relation'].jiufa;
                this.dataTransformOver = true;
                this.$nextTick(() => {
                  var modes = (this.$route.query.category == 1 ? '灸法' : (this.$route.query.category == 2 ? '病症' : '穴位'))
                  this.$refs.igraph.searchWord(this.data['mingcheng'].replace(/\s/g,""), modes)
                })
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
        async tagClick(id, category){
          this.mode = category;
          this.$http.get('/home/InforView', {
            params: {
              'id': id,
              'category': category,
            }
          }).then(res=>{
            this.dataTransformOver = false
            this.data = res.data['data'][0];
            this.relationList.xuewei = res.data['relation'].xuewei;
            this.relationList.bingzheng = res.data['relation'].bingzheng;
            this.relationList.jiufa = res.data['relation'].jiufa;
            this.dataTransformOver = true
          })
        },
        async handleNodeClick(data){
          // 只针对叶子节点
          if(data.id){
            this.mode = data.category;
            this.$http.get('/home/InforView', {
              params: {
                'id': data.id,
                'category': data.category,
              }
            }).then(res=>{
              this.dataTransformOver = false
              this.data = res.data['data'][0];
              this.relationList.xuewei = res.data['relation'].xuewei;
              this.relationList.bingzheng = res.data['relation'].bingzheng;
              this.relationList.jiufa = res.data['relation'].jiufa;
              this.dataTransformOver = true
              this.$nextTick(() => {
                var modes = (data.category == 1 ? '灸法' : (data.category == 2 ? '病症' : '穴位'))
                this.$refs.igraph.searchWord(this.data['mingcheng'].replace(/\s/g,""), modes)
              })
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