<!-- Graph Data Demonstrate -->

<template>
  <div style="height: 800px; background-color: lightblue;">
    <div style="width:90%; height:100px; margin: auto;">
      <el-input
        v-model="searchInput.word"
        class="w-50 m-2"
        size="large"
        placeholder="请输入"
        style="width:200px; margin-top: 30px;"
      />
      <el-button :icon="Search" style="margin-top: 30px; margin-left: 20px;" @click="searchWord(1)">病症</el-button>
      <el-button :icon="Search" style="margin-top: 30px; margin-left: 20px;" @click="searchWord(2)">灸法</el-button>
      <el-button :icon="Search" style="margin-top: 30px; margin-left: 20px;" @click="searchWord(3)">穴位</el-button>
    </div>
    <div ref="graph" style="width:90%; height: 600px; margin:auto; background-color:whitesmoke;"></div>
  </div>
</template>


<script setup>
import {
  Search,
} from '@element-plus/icons-vue'
</script>

<script>
var neo4j = require("neo4j-driver");
export default {
  data() {
    return{
      searchInput: {
        word: "普通感冒"
      },
      echartsData: [],
      nodesRelation: [],
      echartsNode: [],
      myChart: '',
      options: {},
    }
  },

  mounted() {
    // 查询子句
    this.searchWord(1)
  },

  methods:{

    async searchWord(mode){
        var word = this.searchInput.word
        var query = ""
        if(mode === 1){
          query = "MATCH p=(d:病症{name:'"+word+"'})-[:`可用灸法`]->(j:灸法)-[:`治疗"+word+"`]->(x:穴位), q=(d)-[:`属于`]->(l:类别) RETURN p, q"
        }
        else if(mode === 2){
          query = "MATCH p=(j:灸法{name:'"+word+"'})-[:`属于`]->(l:类别) RETURN p"
        }
        else{
          query = "MATCH p=(x:穴位{name:'"+word+"'})-[:`属于`]->(l:类别) RETURN p"
        }
        console.log(query)
        this.executeCypher(query);
    },

    async executeCypher(query) {
      this.echartsNode = []  //节点数组
      this.nodesRelation = [] //关系线数组
      this.echartsData =  [],
      this.category = [] //echarts图例数据数
      // 创建实例
      this.driver = neo4j.driver('neo4j://localhost:7687', neo4j.auth.basic(this.$global.neo4jUserName, this.$global.neo4jUserPassword));
      let me = this;
      me.records = [];
      this.clearAll = true;
      let session = this.driver.session();
      if (query == "") return;
      session.run(query, {}).then((result) => {
        me.clearAll = false;
        me.records = result.records;
        console.log(result.records)
        // 开始处理数据
        for (let i = 0; i < me.records.length; i++) {
          var field_infor = me.records[i]._fields
          for(let j = 0; j < field_infor.length; j++){
            var path_infor = field_infor[j].segments
            for (let k = 0; k < path_infor.length; k++){
              // start
              let startNode = path_infor[k].start
              if (!this.echartsData.some(item => item.name === startNode.properties.name)) {
                this.echartsData.push({
                  name: startNode.properties.name,
                  category: startNode.labels[0]
                })
              }
              // end
              let endNode = path_infor[k].end
              if (!this.echartsData.some(item => item.name === endNode.properties.name)) {
                this.echartsData.push({
                  name: endNode.properties.name,
                  category: endNode.labels[0]
                })
              }
              if (!this.nodesRelation.some(item => (item.source === path_infor[k].start.properties.name && item.target === path_infor[k].end.properties.name))) {
                this.nodesRelation.push({
                  source: path_infor[k].start.properties.name,
                  target: path_infor[k].end.properties.name,
                  name: path_infor[k].relationship.type,
                });
              }
            }
          }
        }
        //提取标签（根据所有的category）
        var arrId = [];
        var legend = [];
        for (var item of this.echartsData) {
          legend.push({ name: item.category })
          if (arrId.indexOf(item.name) == -1) {
            arrId.push(item.name)
            this.echartsNode.push(item);
          }
        }

        this.category = Array.from(new Set(legend))
        session.close();

        this.options = {
          tooltip: {//弹窗
              show: false,
              // enterable: true,//鼠标是否可进入提示框浮层中
              // formatter: formatterHover,//修改鼠标悬停显示的内容
          },
          color:['#fc853e','#28cad8', "#66CCFF", '#99cc66'],
          // 图例设置
          legend: [{
              type: 'scroll',
              orient: 'horizontal',
              itemGap: 40, 
              top: 10,
              left: 'center',
              data: this.category,
          }],
          // 图设置
          series: [
              {
                categories: this.category,
                type: "graph",
                layout: "force",
                zoom: 1.1,
                symbolSize: 50,
                draggable: true,
                roam: true,
                hoverAnimation: true,
                legendHoverLink: false,
                nodeScaleRatio: 0.6,
                focusNodeAdjacency: true,
                edgeSymbol: ["circle", "arrow"],
                edgeSymbolSize: [4, 10],
                // 关系设置
                edgeLabel: {
                    normal: {
                        show: true,
                        textStyle: {
                            fontSize: 10,
                        },
                        formatter(x) {
                            return x.data.name;
                      },
                  },
                },
                // 节点设置
                label: {
                    normal: {
                        show: true,
                        textStyle: {
                            fontSize: 10,
                        },
                        color: "#f6f6f6",
                        textBorderWidth: '1.3',
                        formatter: function (params) {
                            var newParamsName = "";
                            var paramsNameNumber = params.name.length;
                            var provideNumber = 3;
                            var rowNumber = Math.ceil(paramsNameNumber / provideNumber);
                            if (paramsNameNumber > provideNumber) {
                                for (var p = 0; p < rowNumber; p++) {
                                    var tempStr = "";
                                    var start = p * provideNumber;
                                    var end = start + provideNumber;
                                    if (p == rowNumber - 1) {
                                        tempStr = params.name.substring(start, paramsNameNumber);
                                    } else {
                                        tempStr = params.name.substring(start, end) + "\n";
                                    }
                                    newParamsName += tempStr;
                                }
                            } else {
                                newParamsName = params.name;
                            }
                            return newParamsName;
                        },
                    },
                },
                autoCurveness: 0.01,
                // 图谱的关联系数
                force: {
                    repulsion: 200, // 节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                    gravity: 0.01, // 节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                    edgeLength: 200, // 边的两个节点之间的距离，这个距离也会受 repulsion影响 。值越大则长度越长
                    layoutAnimation: true, // 因为力引导布局会在多次迭代后才会稳定，这个参数决定是否显示布局的迭代动画
                    // 在浏览器端节点数据较多（>100）的时候不建议关闭，布局过程会造成浏览器假死。
                },
                data: this.echartsNode,
                links: this.nodesRelation,
              }
            ]
          }
        // 避免重复生成的感叹号报错
        if(this.myChart != null && this.myChart != "" && this.myChart != undefined){
          this.myChart.dispose();
        }
        this.myChart = this.$echarts.init(this.$refs.graph);
        const chart = this.myChart;
        this.myChart.setOption(this.options);
        chart.on('mouseup', function (params) {
          var option = chart.getOption();
          option.series[0].data[params.dataIndex].x = params.event.offsetX;
          option.series[0].data[params.dataIndex].y = params.event.offsetY;
          option.series[0].data[params.dataIndex].fixed = true;
          chart.setOption(option);
        });

      }).catch(function (error) {
        console.log("Cypher 执行失败！", error);
        me.driver.close();
      });

      setTimeout(() => {
        this.knowlegGraphshow = true
       }, 4000);
    },
    closeLoading(status) {
      console.log('closeLoading', status);
    },

  }
}
</script>