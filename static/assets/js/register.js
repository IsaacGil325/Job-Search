function createToast(event){
    if(event.key == 'Enter'){
        let toastcontainer = document.querySelector(".toast-container")
        let fieldentry = document.getElementById("fields-entry")
        let toast = document.createElement("div")
        toast.className = "toast align-items-center"
        let flex = document.createElement("div")
        flex.className = "d-flex"
        let toastbody = document.createElement("div")
        toastbody.className = "toast-body"
        toastbody.innerText = fieldentry.value
        let button = document.createElement("button")
        button.type = "button"
        button.className = "btn-close me-2 m-auto"
        button["data-bs-dismiss"] = "toast"
        fieldentry.value = ""
    }
} 

/*<div class="toast align-items-center" role="alert" aria-live="assertive" aria-atomic="true">
  <div class="d-flex">
    <div class="toast-body">
    Hello, world! This is a toast message.
   </div>
    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
</div>*/