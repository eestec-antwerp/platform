<template>
<div>
	<div class="showcase-wrapper sticky">
		<div class="showcase-text">Welcome to EESTEC Antwerpen!</div>
	</div>

	<news></news>
	
	<div class="container">
		<div class="more"><div><router-link to="/news">
			<button type="button" class="btn btn-default">More ...</button>
		</router-link></div></div>
	</div>
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

.more {
	display: flex;
	justify-content: center;
/* 	align-items: center; */
}
</style>
