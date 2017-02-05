<template>

<ul class="mainmenu">
	<li :class="{active: $route.path == '/'}">
		<router-link to="/"> Home </router-link>
	</li>

	<li :class="{active: $route.path.startsWith('/news')}">
		<router-link to="/news/"> News </router-link>
	</li>

	<li :class="{active: $route.path.startsWith('/about')}">
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

.mainmenu .active {
	font-weight: bold;
}

</style>
