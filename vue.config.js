module.exports = {
  lintOnSave: true,
  
  configureWebpack:{
    devtool: 'source-map'
  },
  devServer: {
    disableHostCheck: true,
    proxy: 'http://localhost:8080'
  },

  transpileDependencies: ['vue-world-map', 'vuetify'],

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false,
    },
  },
}
