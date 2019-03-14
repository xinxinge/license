<template>
  <div class="login-container">
      <div class="textType"><router-link to="/register">查看</router-link></div>
      <div class="textType1" @click="getData">注册</div>
  </div>
</template>
<script>
  import fetchServer from '../../server/data.js'
    export default {
        name: "Login",
      data(){
        return{
          message:'',
          address: ''
        }
      },
      methods:{
        getData(){
          fetchServer({
            callback: (res) => {
              if (res.code == 0) {
                this.$store.commit("set_list", res.data)
                this.$router.push({path:'/choose'})
              } else {
              }
            },
            url: '/v1/Product_list',
            method: 'get',
          })
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
    a {
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
      color: $light_gray;
      left:50%;
      top:50%;
    }
  }
</style>
