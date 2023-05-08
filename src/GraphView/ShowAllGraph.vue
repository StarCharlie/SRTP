<!-- Graph Data Demonstrate -->
<template>
  <el-row :gutter="20">
      <!-- 左边栏 -->
      <el-col :span="4">
        <div style="background-color: aliceblue;">
          <div v-if="this.dataTransformOver" style="margin-top: 50px;">
              <el-input
                v-model="filterText"
                style="width: 80%; margin-left: 20px;"
                placeholder="输入关键词"
              />
              <el-tree
                :data="menuList"
                node-key="label"
                :default-expanded-keys="word"
                highlight-current
                :props="defaultProps"
                accordion
                :current-node-key="word"
                @node-click="handleNodeClick"
                :filter-node-method="filterNode"
                ref="tree"
                style="width: 80%; margin-left: 20px; margin-top: 10px"
              />
          </div>
        </div>
      </el-col>
      <el-col :span="20">
        <div style="height:800px">
          <GraphInfor ref="igraph"></GraphInfor>
        </div>
      </el-col>
  </el-row>
  <el-divider>
    <el-icon><star-filled /></el-icon>
  </el-divider>
  <div class="centered">
    <p class="title-info">--数据来源--</p>
    <p class="project-info">关系抽取：《实用常见病艾灸疗法》、《零基础学中医艾灸》、《艾灸穴位新解》、《简易针灸治疗法(艾灸篇)》</p>
  </div>
</template>


<script setup>
import { StarFilled } from '@element-plus/icons-vue'
</script>

<script>
import GraphInfor from "./GraphInfor.vue"
export default {
  name: "GraphInfor",
  components:{
    GraphInfor,
  },
  data() {
    return{
      menuList: null,
      filterText: "",
      dataTransformOver: false,
    }
  },

  mounted() {
    this.menuList =  JSON.parse(window.sessionStorage.getItem('menuList'))
    this.dataTransformOver = true;
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val.trim())
    },
  },

  methods:{
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    handleNodeClick(data){
      this.$nextTick(() => {
        this.$refs.igraph.handleNodeClick(data)
      })
    }
  }
}
</script>

<style>
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