<template>
<router-link class="article-summary" :to="{path: '/article/' + article.slug + '/'}">
	<div>
		<time class="pull-right post-list">{{article.date}}</time>
		<div class="article-summary-title">{{article.title}}</div>
	</div>
	{{article.summary}}
</router-link>
</template>

<script>
export default {
	data() {
		return {}
	},
	props: ['article'],
}
</script>

<style lang="scss">
@import "./style/variables.scss";
</style>
