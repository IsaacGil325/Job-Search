function getDelete(job_id) {
  var title = document.getElementById("job_title_"+job_id).innerText;
  // var c_name = document.getElementById("company_name_"+job_id).innerText;
  // var job_location = document.getElementById("job_location_"+job_id).innerText;
  // var job_description = document.getElementById("job_description_"+job_id).innerText;

  console.log('job id:', job_id);
  $.ajax({
    type: "POST",
    url: "delete_job",
    data: JSON.stringify({
      "job_id": job_id,
      "job_title": title//,
      // "company_name": c_name,
      // "location": job_location,
      // "description": job_description,
    }),
    contentType: "application/json",
    dataType: 'json'
  });

}