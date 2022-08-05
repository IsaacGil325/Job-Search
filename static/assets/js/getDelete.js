function getDelete(job_id) {
  var title = document.getElementById("job_title_"+job_id).innerText;
  // var c_name = document.getElementById("company_name_"+job_id).innerText;
  // var job_location = document.getElementById("job_location_"+job_id).innerText;
  // var job_description = document.getElementById("job_description_"+job_id).innerText;

  let theTable = document.querySelector("tbody");
  let theRow = document.getElementById(job_id);
  allRows = Array.from(theTable.children)
  jobPos = allRows.indexOf(theRow) + 1;

  for(let i=jobPos; i<allRows.length; i++){
    currentRow = theTable.children[i];
    currentRowNum = parseInt(currentRow.children[0].innerText);
    currentRow.children[0].innerText = `${currentRowNum - 1}`;
  }

  // trying to fade out the removal of a table row
  // theRow.style.display = 'none';
  // theRow.style.transition = 'display 1s';
  // theRow.style.webkitTransition = 'display 1s';
  // theRow.style.oTransition = 'display 1s';
  // theRow.style.msTransition = 'display 1s';
  // theRow.style.mozTransition = 'display 1s';
  theRow.remove();

  // console.log('job id:', job_id);
  $.ajax({
    type: "DELETE",
    url: "delete_job",
    data: JSON.stringify({
      "job_id": job_id//,
      // "job_title": title // had it for debugging purposes on the backend to print the title
    }),
    contentType: "application/json",
    dataType: 'json'
  });

}