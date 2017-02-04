<template>
<div class="container">
	<newscard :article="article" v-for="article in articles"></newscard>
</div>
</template>

<script>
import newscard from './newscard'

export default {
	data() {
		return {
			articles: [
				{
					id: "security-talk",
					date: "Some day?",
					title: "Security talk blabla",
					summary: "Bank van breda doet security stuff",
				}, {
					id: "new-website",
					date: "Some other day?",
					title: "We have new website",
					summary: "Look at crazy Vue.js",
				}
			]
		}
	},
	components: {
		newscard: newscard
	}
}
</script>

<style lang="scss">
@import "./style/variables.scss";
</style>
