<template>
  <!--  <div class="hello">-->
  <!--    <div>{{ node_right }}</div>-->
  <!--    <div>-->
  <!--      <div v-for="node in node_list">{{node}}</div>-->
  <!--    </div>-->
  <!--    <div>{{ update_time }}</div>-->
  <!--  </div>-->
  <el-container style="width: 800px">
    <el-main>
      <!--      <el-header content="详情页面">-->
      <!--      </el-header>-->
      <!--      <el-card v-for="node in node_list" class="box-card">-->
      <!--        <div slot="header" class="clearfix; width: 200px">-->
      <!--          <span>{{node.name}}</span>-->
      <!--        </div>-->
      <!--        <div class="text item">inner_ip:{{node.inner_ip}}</div>-->
      <!--        <div class="text item"><span>outer_ip:{{node.outer_ip}}</span></div>-->
      <!--        <div class="text item"><span>online_time:{{node.online_time}}</span></div>-->
      <!--&lt;!&ndash;        <div v-for="o in 4" :key="o" class="text item">&ndash;&gt;-->
      <!--&lt;!&ndash;          {{ '列表内容 ' + o }}&ndash;&gt;-->
      <!--&lt;!&ndash;        </div>&ndash;&gt;-->
      <!--      </el-card>-->
      <el-table :data="node_list">
        <el-table-column prop="inner_ip" label="内网IP" width="140">
        </el-table-column>
        <el-table-column prop="name" label="别名" width="120">
        </el-table-column>
        <el-table-column prop="outer_ip" label="外网IP">
        </el-table-column>
        <el-table-column prop="online_time" label="更新时间">
        </el-table-column>
      </el-table>
      <el-row>
        <el-col :span="24">
          <div v-if="node_right">
            <i class="el-icon-circle-check"></i>
            <span>接口正常</span>
          </div>
          <div v-else>
            <span>接口错误</span>
            <i class="el-icon-circle-close"></i>
          </div>
        </el-col>
        <el-col>
          <div v-if="update_time">更新时间: {{ update_time }}</div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: '',
      node_right: false,
      node_list: [],
      update_time: null
    }
  },
  created() {
    this.$axios({
      method: 'get',
      url: 'http://al.bigf00t.net:7789/status?key=whoami'
    }).then((response) => {
      // console.log(response)
      let ret_data = response.data;
      console.log(ret_data);
      if (ret_data.code === 0) {
        this.node_right = true;
        this.node_list = ret_data.data.node;
        this.update_time = ret_data.data.update_time;
      } else {
        this.node_right = false;
      }
    }).catch((error) =>
      console.log(error))
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.el-row {
  margin-bottom: 20px;


}
.el-col {
  border-radius: 4px;
}
</style>
