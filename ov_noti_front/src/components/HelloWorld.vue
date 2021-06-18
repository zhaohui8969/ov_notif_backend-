<template>
  <!--  <div class="hello">-->
  <!--    <div>{{ node_right }}</div>-->
  <!--    <div>-->
  <!--      <div v-for="node in node_list">{{node}}</div>-->
  <!--    </div>-->
  <!--    <div>{{ update_time }}</div>-->
  <!--  </div>-->
  <el-container style="width: 400px">
    <el-main>
      <el-table :data="node_list" style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand" size="mini">
              <!--              <el-form-item label="别名"><span>{{ props.row.name }}</span></el-form-item>-->
              <!--              <el-form-item label="内网IP"><span>{{ props.row.inner_ip }}</span></el-form-item>-->
              <el-form-item label="外网IP"><span>{{ props.row.outer_ip }}</span></el-form-item>
              <el-form-item label="更新时间"><span>{{ props.row.online_time }}</span></el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="别名"></el-table-column>
        <el-table-column prop="inner_ip" label="内网IP"></el-table-column>
      </el-table>
      <el-row>
        <el-col :span="24">
          <div v-if="node_right === true">
            <i class="el-icon-circle-check"></i>
            <span>接口正常</span>
          </div>
          <div v-else-if="node_right === false">
            <i class="el-icon-circle-close"></i>
            <span>接口错误</span>
          </div>
          <div v-else>
            <i class="el-icon-loading"></i>
            <span>数据加载中</span>
          </div>
        </el-col>
        <el-col>
          <div v-if="update_time">更新时间: {{ update_time }}</div>
        </el-col>
      </el-row>
      <el-button type="primary" :disabled="node_right === null" v-on:click="fetch_data" style="width: 100%">
        更新
      </el-button>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: '',
      node_right: null,
      node_list: [],
      update_time: null
    }
  },
  methods: {
    fetch_data() {
      this.node_right = null;
      this.$axios({
        method: 'get',
        url: 'http://al.bigf00t.net:7789/status?key=whoami'
      }).then((response) => {
        // console.log(response)
        let ret_data = response.data;
        // console.log(ret_data);
        if (ret_data.code === 0) {
          this.node_right = true;
          this.node_list = ret_data.data.node;
          this.update_time = ret_data.data.update_time;
        } else {
          this.node_right = false;
        }
      }).catch((error) =>
        console.log(error))
      // setTimeout(this.fetch_data, 1);
    },
  },
  created() {
    this.fetch_data();
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
  margin: 10px;
}

.el-col {
  border-radius: 4px;
}
</style>
