<template>
<transition name="fade">
<div class="alert" v-if="status != null" :class="'alert-' + status">
	{{message}}
</div>
</transition>
</template>

<script>
export default {
	data: () => {
		return {}
	},
	props: {
		status: {
			default: () => null,
		},
		message: {
			default: () => "",
		}
	}
}
</script>

<style lang="scss">

</style>
