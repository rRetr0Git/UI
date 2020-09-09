module.exports = {
    proxy: {
        '/api': {
            target: 'http://47.106.64.141:9080',
            changeOrigin: true,
            pathRewrite: {
                "^/api": ''
            }
        }
    }
}