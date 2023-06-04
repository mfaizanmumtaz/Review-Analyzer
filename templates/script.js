const responsePara = document.getElementById("response")
const button = document.getElementsByTagName("button")[0]
const form = document.getElementById("form")
var csrfToken = "{{ csrf_token }}";
let task = ""
const autoOption1 = document.getElementById("autoOption1")
function autoOption() {
    autoOption1.innerHTML = `
    <div class="flex space-x-2 text-gray-400"><input class="options" type="radio" name="radioGroup" value="Review Response"><span
        class="text-xs px-2">Generate Review Response</span></div>
        <div class="flex space-x-2 text-gray-400"><input type="radio" class="options"  name="radioGroup" value="Review Summary"><span class="text-xs px-2">Generate Review
            Summary</span></div>
            <div class="flex space-x-2 text-gray-400"><input type="radio" class="options"  name="radioGroup" value="Review Sentiment"><span class="text-xs px-2">Generate Review
                Sentiment</span></div>`
    const options = document.querySelectorAll(".options")
    options.forEach(element => {
        element.addEventListener("click", function () {
            task = this.value
        })
    })
    options[0].click()
};

const AIwriter = ((response) => {
    button.removeAttribute("disabled")
    responsePara.innerHTML = ` <div class="w-full bg-gray-700 text-gray-400 px-4 py-4 flex flex-col items-center justify-center space-y-6">
            <span class="w-full text-sm md:text-base font-semibold text-white">Task Title: (${task})</span>
            <p class="w-full text-sm md:text-base">${response}
            </p>
            <button type="submit" class="bg-green-500 text-white p-2 rounded-sm px-4 text-sm font-bold">Copy</button></div>`
})
const loading = (() => {
    button.setAttribute("disabled", true)
    responsePara.innerHTML = `<div class="w-full bg-gray-700 py-4 text-center">
<span class="text-white">Please wait...</span></div>`
})
const NetWorkError = (() => {
    button.removeAttribute("disabled")
    responsePara.innerHTML = `<div class="w-full bg-gray-700 py-4 text-center"><span class="text-center text-red-500">There is some error!</div></span>`
})
form.addEventListener("submit", (event) => {
    event.preventDefault()
    loading()
    formdata = new FormData(form)
    fetch("/", {
        method: "POST", headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }, body: formdata
    }).then((response) => {
        if (response.status === 200) {
            return response.json()
        }
    }).then((response) => {
        AIwriter(response)
    }).catch(() => {
        NetWorkError()
    })
})