function getResults(job_id) {
  console.log('from getResults:')
  
  var title = document.getElementById("job_title_"+job_id).innerText;
  var c_name = document.getElementById("company_name_"+job_id).innerText;
  var job_location = document.getElementById("job_location_"+job_id).innerText;
  var job_description = document.getElementById("job_description_"+job_id).innerText;
  console.log('job id:', job_id)
  console.log(job_description)
  // console.log(title)
  // console.log(c_name)
  // console.log(job_location)
  // console.log(job_desciption)
  $.ajax({
    type: "POST",
    url: "saved_jobs",
    data: JSON.stringify({
      "job_id": job_id,
      "job_title": title,
      "company_name": c_name,
      "location": job_location,
      "description": job_description,
    }),
    contentType: "application/json",
    dataType: 'json'
  });
}
