<template>
  <div>
    <br/>
    <el-table
      :data="getData1"
      style="width: 100%" :row-style="tableRowStyle"
      :header-cell-style="tableHeaderColor">
      <el-table-column type="selection" width="45"></el-table-column>
      <el-table-column
        prop="name"
        label="产品名称"
        style="width: 50%">
      </el-table-column>
      <el-table-column
        prop="abbreviation"
        label="产品缩写"
        style="width: 50%">
      </el-table-column>
    </el-table>
    <el-button type="primary"
               style="width:100%;margin-bottom:30px;"
    @click="handleClick">确定</el-button>
  </div>
</template>
<script>
  import store from '@/store/index'
    export default {
        name: "Droduct",
      store,
      data(){
          return{
            name:'',
            abbreviation: '',
            current:''
          }
      },
      methods:{
        tableRowStyle({ row, rowIndex }) {
          return 'background-color: #2d3a4b;color: #eee;font-weight: 500; !important'
        },
        // 修改table header的背景色
        tableHeaderColor({ row, column, rowIndex, columnIndex }) {
          if (rowIndex === 0) {
            return 'background-color: #2d3a4b;color: #eee;font-weight: 500;'
          }
        },
        handleClick(){
          this.$router.push({path:'/register'})
        }
      },
      computed:{
        getData1(){
          return this.$store.state.dcArr
        }
      }
    }
</script>

<style rel="stylesheet/scss" lang="scss">
  $light_gray: #eee;
  $bg: #2d3a4b;
  el-table{
    background:$bg ;
     margin-left: 20px;
   }
  span {
    margin-top: 30px;
  }
  li.active{
    background: red;
  }
</style>
