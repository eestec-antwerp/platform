<template>

<ul>
	<li class="active">
		<router-link to="/"> Home </router-link>
	</li>

	<li>
		<router-link to="/news/"> News </router-link>
	</li>

	<li>
		<router-link to="/about/"> About </router-link>
	</li>
</ul>
</template>

<script>
export default {
    data() {
        return {}
    }
}
</script>

<style lang="scss">
@import "./style/variables.scss";
</style>
