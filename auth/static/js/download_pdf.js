$(document).ready(()=>{

    let attemps = 0

    $.ajax({
        url: '/file/file.pdf',
        method: 'GET',
        xhrFields :{
          responseType: 'blob'
        },
        success : function(data){
            let a = document.createElement('a');
            let url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'file.pdf';
            document.body.append(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            attemps=4
          }
        })

   
  })