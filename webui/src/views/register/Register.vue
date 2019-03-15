<template>
  <div class="login-container">
    <el-form class="login-form"
             autoComplete="on"
             :model="loginForm"
             ref="loginForm"
             label-position="left">
      <div class="title-container">
        <h3 class="title">系统注册</h3>
        <!-- <h3 class="title">{{$t('login.title')}}</h3> -->
        <!-- <lang-select class="set-language"></lang-select> -->
      </div>
      <el-form-item prop="username">
        <span class="spanColor">
            用户 :
        </span>
        <el-input name="username"
                  type="text"
                  v-model="loginForm.name"
                  autoComplete="on"
                  placeholder="username" />
      </el-form-item>
      <el-form-item prop="username">
        <span class="spanColor">
            序列号 :
        </span>
        <el-input name="username"
                  type="text"
                  v-model="loginForm.product_id"
                  autoComplete="on"
                  placeholder="username" />
      </el-form-item>
      <el-form-item prop="username">
        <span class="spanColor">
            注册类型 :
        </span>
        <el-input name="username"
                  type="number"
                  v-model="loginForm.status"
                  autoComplete="on"
                  placeholder="username" />
      </el-form-item>
      <el-form-item prop="username" class="spanColor">
        注册日期 :
        <el-input name="username"
                  type="text"
                  v-model="loginForm.date"
                  autoComplete="on"
                  placeholder="username" />
      </el-form-item>
      <el-form-item prop="password">
        <span class="spanColor">
            有效期 :
        </span>
        <el-input name="password"
                  type="number"
                  @keyup.enter.native="handleLogin"
                  v-model="loginForm.day"
                  autoComplete="on"
                  placeholder="password" />
      </el-form-item>
      <el-button type="primary"
                 style="width:100%;margin-bottom:30px;"
                 :loading="loading"
                 @click.native.prevent="handleLogin">提交</el-button>
    </el-form>
  </div>
</template>
<script>
  import fetchServer from '../../server/data.js'
    export default {
        name: "Register",
      data(){
        return {
          loginForm: {
            name: 'admin', //
            product_id: 'DC00000001', //
            status: 1,
            date: '2019-3-13',
            day: 60
          },
          passwordType: 'password',
          loading: false,
          showDialog: false,
        }
      },
      methods: {
        handleLogin() {
          fetchServer({
            callback: (res) => {
              if (res.code == 1) {
                this.$router.push({path:'/'})
              } else {
              }
            },
            url: '/v1/Register_code',
            method: 'post',
            data: this.loginForm
          })
         /* this.$axios.post('/upload/v1/Register_code',this.loginForm)
            .then(function (response) {
              if(response.data.code === 0){
                this.code = response.data.message
              }
            })
            .catch(function (error) {
              console.log(error);
            })*/
        }
      }
    }
</script>

<style rel="stylesheet/scss" lang="scss">
  $bg: #2d3a4b;
  $light_gray: #eee;

  /* reset element-ui css */

  .login-container {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;
      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        &:-webkit-autofill {
          box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: #fff !important;
        }
      }
    }
    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;
  .login-container {
    position: fixed;
    height: 100%;
    width: 100%; // background-image:'../../../'
    background-color: $bg;
    .textType{
      color: $light_gray;
      text-align: right;
    }
    .spanColor{
      color: $light_gray;
      margin-left: 5px;
      text-align: center;
    }
    .login-form {
      position: absolute;
      left: 0;
      right: 0;
      width: 520px;
      padding: 35px 35px 15px 35px;
      margin: 120px auto;
    }
    .tips {
      font-size: 14px;
      color: #fff;
      margin-bottom: 10px;
      span {
        &:first-of-type {
          margin-right: 16px;
        }
      }
    }
    .title-container {
      position: relative;
      .title {
        font-size: 26px;
        font-weight: 400;
        color: $light_gray;
        margin: 0px auto 40px auto;
        text-align: center;
        font-weight: bold;
      }
      .set-language {
        color: #fff;
        position: absolute;
        top: 5px;
        right: 0px;
      }
    }
    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      color: $dark_gray;
      cursor: pointer;
      user-select: none;
    }
    .thirdparty-button {
      position: absolute;
      right: 35px;
      bottom: 28px;
    }
  }
</style>
