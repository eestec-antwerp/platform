<template>
<div class="showcase-wrapper sticky">
	
	<div class="showcase-text">Welcome to EESTEC Antwerpen!</div>
	
</div>

<div class="container">
	
	<news></news>
	
</div>

</template>

<script>
import news from './news';

export default {
	data() {
		return {}
	},
	components: {
		news: news
	}
}
</script>

<style lang="scss">
@import "./style/variables.scss";
</style>
