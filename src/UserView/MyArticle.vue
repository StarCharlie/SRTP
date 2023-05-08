<template>
  <div style="background-color: rgba(239, 250, 246, 0.53)">
    <br />

    <br />
    <div style="width: 100%; margin-left: 1%" class="main">
      <el-row :gutter="20">
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
                    <h2 id="title" v-html="item['title']"></h2>
                    <!-- 总有一天我会把这个逆天操作改掉 -->
                    <el-tag class="ml-2" size="large" :type="index_translate(item['category'])[1]" >{{ index_translate(item['category'])[0] }}</el-tag>
                    <p id="infor">{{ highLight(item['infor']) }}</p>
                  </el-col>
                  <!-- 按钮部分 -->
                  <el-col :span="5">
                    <div style="text-align: -webkit-center">
                      <el-button type="primary" style="width:150px" @click="toInfor(item['id'],  item['category'])">详情</el-button>
                    </div>
                    <br/>
                    <div style="text-align: -webkit-center">
                      <el-button type="info" style="width:150px" @click="nolike(item['id'],  item['category'])">取消收藏</el-button>
                    </div>
                  </el-col>
                </el-row>
              </el-card>
              <div style="margin-top: 50px; margin-left: 20px; margin-bottom: 50px;">
                <el-pagination
                  @size-change="getInfor()"
                  @current-change="getInfor()"
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
    </div>
    <br />
    <div class="footer" style="margin: 0 auto; width: 100%">
      <div class="block">
        <el-pagination
          background
          layout="total, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>


<script>


export default {
  data() {
    return {
      data: null,
      total: 2,
      user_id: "",
      Messages: null,
      favor: {
        infor_category: "",
        user_id: "",
        infor_id: "",
      },
      transform: {
        user_id: 0,
        page_number: 1,
        page_size: 10,
      },
    };
  },
  created(){
      this.transform['user_id'] = (this.$cookies.get('id') == null) ? -1 : this.$cookies.get('id');
      this.getInfor();
  },
  methods: {
      index_translate(category){
        if(category == 1) return ["灸法", "info", 1]
        else if(category == 2) return ["病症", "warning", 2]
        else return ["穴位", "success", 0]
      },
      highLight(str){
          if(str.length >= 80) str = str.substring(0, 80) + "...";
          return str
      },
      async getInfor(){
        this.$http.post('/user/UserLikeList', this.transform).then(res=>{
              this.data = res.data['data'];
              this.total = res.data['totalNumber'];
          });
      },
      async nolike(id, category){
            this.favor['user_id'] = (this.$cookies.get('id') == null) ? -1 : this.$cookies.get('id');
            this.favor['infor_id'] = id;
            this.favor['infor_category'] = category;
            this.$http.post('/user/UserDislike', this.favor).then(res=>{
              if(res.data['message'] == "success"){
                alert("取消收藏成功");
                this.$router.go(0)
              }
              else alert(res.data['message']);
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
  },
}
</script>

<style scoped>
.message {
  width: 25em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.image{
  margin-top: 40px;
  height: 100px; 
  width: 200px;
}
.el-card{
  margin-top: 50px;
}
</style>
