
module.exports = {
	devtool: '#eval-source-map',
	entry: './main.js',
	output: {
		path: './build',
		filename: 'app.bundle.js'
	},
	module: {
		// `loaders` is an array of loaders to use.
		// here we are only configuring vue-loader
		loaders: [
			{
				test: /\.vue$/, // a regex for matching all files that end in `.vue`
				loader: 'vue'   // loader to use for matched files
			},
			{
				test: /\.json$/,
				loader: 'json'
			},
			{
		      test: /\.js$/,
		      exclude: /(node_modules|bower_components)/,
		      loader: 'babel',
		      query: {
		        presets: ['es2015']
		      }
		  	},
			{
				test: /\.(jpe?g|png|gif|svg)$/i,
				loaders: [
					'file?hash=sha512&digest=hex&name=[hash].[ext]',
					'image-webpack?bypassOnDebug&optimizationLevel=7&interlaced=false'
				]
			},
			{
  				test: /\.scss$/,
  				loaders: ["style", "css", "sass"]
			},
		]
	},
	resolve: {
		extensions: ['', '.webpack.js', '.web.js', '.js', '.vue', '.json'],
		alias: {
			'vue$': 'vue/dist/vue.common.js'
		}
	},
	vue: {
  		loaders: {
    		'scss': 'vue-style!css!sass'
  		}
	},
};
