<template>
  <div class="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-2xl font-semibold text-gray-700 mb-4">提交作业</h2>

    <!-- 用户名 -->
    <div class="mb-4">
      <label for="student_id" class="block text-gray-600 text-sm font-medium">学号:</label>
      <input
        id="student_id"
        v-model="student_id"
        type="text"
        class="mt-2 block w-full text-sm text-gray-900 border border-gray-300 rounded-lg focus:outline-none"
      />
    </div>

    <!-- 选择文件 -->
    <div class="mb-4">
      <label class="block text-gray-600 text-sm font-medium">选择文件:</label>
      <input
        type="file"
        @change="handleFileChange"
        class="mt-2 block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none"
        accept=".zip"
      />
      <p v-if="file" class="mt-2 text-gray-500 text-sm">已选择: {{ file.name }}</p>
    </div>

    <button
      @click="submitAssignment"
      :disabled="uploading"
      class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition disabled:bg-gray-400"
    >
      {{ uploading ? '提交中...' : '提交作业' }}
    </button>

    <p v-if="successMessage" class="mt-3 text-green-600 text-sm font-medium">
      {{ successMessage }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const student_id = ref('')
const file = ref(null)

const uploading = ref(false)
const successMessage = ref('')

function handleFileChange(event) {
  file.value = event.target.files[0]
}

const submitAssignment = async () => {
  if (!student_id.value) {
    alert('请填写学号')
    return
  }

  if (!file.value) {
    alert('请上传作业文件')
    return
  }

  uploading.value = true

  const formData = new FormData()
  formData.append('student_id', student_id.value)
  formData.append('file', file.value)

  // 后端API
}
</script>
