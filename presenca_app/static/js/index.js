modal = document.getElementById('modal')
form_user = document.getElementById('form-user')
nome_porf = document.getElementById('nome-prof')
form = null
button = null
loading = document.getElementById('loading')
var dataAtual = new Date();
        var hora = dataAtual.getHours();
        var minutos = dataAtual.getMinutes();
function mostrarAviso(text, color="#e93f4f") {
  var aviso = document.getElementById('aviso');
  aviso.textContent = text
  aviso.style.backgroundColor =  color
  aviso.classList.remove('esconder');
  setTimeout(function() {
    aviso.classList.add('esconder');
  }, 5000); // Oculta o aviso após 3 segundos (3000 milissegundos)
}

document.querySelectorAll('.Retirar').forEach((btn) => {
    btn.addEventListener('click', (event) =>{

        event.preventDefault();
        modal.style.display = 'block';
        form = btn.closest('form');
        button = btn

    })
})
document.querySelectorAll('.Devolver').forEach((btn) => {
    btn.addEventListener('click', (event) =>{

        event.preventDefault();
        modal.style.display = 'block';
        form = btn.closest('form');
        button = btn
    })
})

document.querySelector('#btn-user').addEventListener('click', (event) => {
    event.preventDefault();
    registraHora();
});
function limparForm(form_user){
    for (var i = 0; i < form_user.elements.length; i++) {
  var element = form_user.elements[i];


  if (element.type === 'text' || element.type === 'password') {

    element.value = '';
  }
}
}

// Fechar modal ao clicar no botão de fechar
document.querySelector('#fechar').addEventListener('click', function() {
    modal.style.display = 'none';
    limparForm(form_user)
});


function registraHora(){
    console.log('Passou aqui no fetch')

    button.disabled = true;
    loading.style.display = 'flex'

    nome_porf.value = form.querySelector('[name="registro_id"]').value;

    fetch(form_user.action, {
        method: form.method,
        body: new FormData(form_user),
    }).then(function(data) {
        return data.json()
    }).then(function(response){
        button.disabled = false;
        if (response.success) {
            mostrarAviso(response.success_message, '#88e93f')
            modal.style.display = 'none';
            limparForm(form_user)
            fetch(form.action, {
                method: form.method,
                body: new FormData(form),
                }).then(function(data) {
                    return data.json()
                }).then(function(response){
                    if (response.success) {
                        button.disabled = false;
                      if (button.classList.contains('Retirar')) {
                        button.textContent = `Retirou ${response.hora}`;
                        button.style.backgroundColor = 'green';
                      } else if (button.classList.contains('Devolver')) {
                        button.textContent = `Devolvido ${response.hora}`;
                        button.style.backgroundColor = 'green';
                      }
                    }})
                .catch(function(error) {

                })
        }
        else{
        mostrarAviso(response.error_message)
        }
        })
        .finally(function(){
        loading.style.display = 'none'
        })
}