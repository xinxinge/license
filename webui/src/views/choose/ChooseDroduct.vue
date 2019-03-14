<template>
  <div class="login-container">
    <el-container>
      <el-header>
        <div class="title-container">
          <div class="from-div">
            选择正式还是试用<br/>
            <input type="radio" name="test" value="试用" checked="checked"> 试用
            <input type="radio" name="test" value="正式"> 正式
          </div>
        </div>
      </el-header>
      <Droduct></Droduct>
    </el-container>
  </div>
</template>

<script>
  import Droduct from '@/views/droduct/Droduct'
    export default {
        name: "ChooseDroduct",
      components: {
        Droduct,
      },
      computed: {
          dcList(){
            return this.$store.dcArr
          }
      }
    }
</script>

<style rel="stylesheet/scss" lang="scss" >
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;
  .login-container {
    position: fixed;
    height: 100%;
    width: 100%; // background-image:'../../../'
    background-color: $bg;
    margin: auto;
    a{
      text-decoration: none;
      color: $light_gray;
    }
    .textType{
      text-align: center;
      margin-top: 35%;
      left:50%;
      top:50%;
    }
    .textType1{
      text-align: center;
      margin-top: 30px;
      left:50%;
      top:50%;
    }
    .title-container {
      position: absolute;
      padding-top: 20px;
      padding-bottom: 20px;
      width: 100%;
      .from-div {
        position: absolute;
        top: 50%;
        left:50%;
        transform: translate(-50%,-50%);
        color: $light_gray;
        margin-top: 30px;
      }
      input{
        margin-top: 10px;
        align-content: center;
      }
    }
  }
</style>
