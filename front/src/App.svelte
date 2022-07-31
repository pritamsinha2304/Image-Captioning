<script lang="js">
  import { NotificationDisplay, notifier } from '@beyonk/svelte-notifications'
  import { Jellyfish } from 'svelte-loading-spinners'
  
  let fileVar;
  let fileName;
  let imageAvatar;
  let success_data;
  let error_data;
  let inputDisabled = false;

  async function post_form(){

    inputDisabled = true;

    let formData = new FormData();
    if (fileVar && fileVar[0]){
      formData.append("imagefileinput", fileVar[0], fileVar[0].name);

      await fetch('/post', {
        method: "POST",
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: formData
      })
      .then(response => response.json())
      .then((data) => {        
        console.log(data);
        if ("success" in data['response']){
          success_data = data['response']['success'];
          notification("success", "File Uploaded Successfully");
        }
        if ("error" in data['response']){
          error_data = data['response']['error'];
          notification("error", error_data);
        }
        inputDisabled = false;
      })
      .catch(err => {
        notification("error", err);
        inputDisabled = false;
      })
    }
  }

  const showcaseImage = (e) => {
    let image = e.target.files[0];
    fileName = e.target.files[0].name;
    let reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = e => {
      imageAvatar = e.target.result;
    }
  }

  /**
  * @param {string} msg_type
  * @param {string} msg
  */
  function notification(msg_type, msg){
    if (msg_type == "error"){
      notifier.danger(msg, 3000);
    }
    if (msg_type == "success"){
      notifier.success(msg, 3000);
    }
  }

</script>

<main>

  <NotificationDisplay />

  <div class="px-5 py-3 bg-gray-100 mx-12 mt-5 text-center text-3xl rounded-md">
    Image Captioning
    <div class="bg-gray-200 rounded-md my-2 text-black p-5 hover:shadow-2xl ease-in-out duration-300 text-justify text-xl">
      <p>Images are nowadays became an essential component of our living. Each image we collected, clicked, snapped holds an important
      message to the people around that person. Each image tells a story around the event happened during the clicking of the image.
      Besides these, the images holds many information that can describes the whole image in a nutshell.</p> 
      <br/>
      <p><span class="font-semibold">Image Captioning</span> is a field of AI which can take an image and extract all the necessary information from it and can describe that image in a nutshell.
      It can be appied in various fields based on requirements. Though it's main use is in <q class="font-semibold">describing the image</q>.</p>  
    </div>
  </div>

  <div class="p-1 bg-gray-100 mx-12 mt-5 mb-8 rounded-md flex flex-row align-middle items-center">
    <div class="bg-gray-200 rounded-md p-3 text-black grow mx-3 my-5 hover:shadow-2xl ease-in-out duration-300">
      <span class="text-3xl">Upload Image</span>
      <div class="rounded-md bg-amber-200 px-5 py-1 mt-3 mb-1 mx-5 text-lg">
        Allowed Image Format: <span class="font-semibold">jpg</span>, <span class="font-semibold">png</span>
      </div>
      <form class="py-2" on:submit|preventDefault={post_form}>
        <input type="file" name="imagefileinput" id="imagefile" class="rounded-lg w-full text-gray-700 border-2 border-gray-700 my-2 text-2xl" required accept="image/jpeg, image/png" bind:files={fileVar} on:change={(e)=>showcaseImage(e)} disabled={inputDisabled}/>
        <br/>
        {#if !inputDisabled}
          <input type="submit" value="Submit" class="w-full ease-in-out duration-300 text-gray-700 hover:text-white text-2xl border-2 border-gray-700 rounded-lg hover:bg-gray-700" disabled={inputDisabled}/>
        {/if}
      </form>
      {#if inputDisabled}
        <div class="w-full ease-in-out duration-300 text-gray-700 hover:text-white text-2xl border-2 border-gray-700 rounded-lg hover:bg-gray-700 flex items-center text-center align-middle content-center justify-center shadow-2xl">
          <Jellyfish size="60" color="currentColor" unit="px" duration="2s"></Jellyfish>
          <span class="text-2xl ml-5">Processing...</span>
        </div>
      {/if}
    </div>
    {#if imageAvatar}
      <div class="rounded-md p-1 shadow-2xl bg-gray-100 ease-in-out duration-300">
        <img class="w-44 rounded-md object-cover" src="{imageAvatar}" alt="avatar"/>
        <div class="text-center">{fileName}</div>
      </div>
    {/if}
  </div>

  {#if success_data}
    <div class="mx-12 mt-3 mb-10 p-3 text-center rounded-md bg-green-100 text-2xl"> 
      {success_data}
    </div>
  {/if}

</main>


<style>
</style>
