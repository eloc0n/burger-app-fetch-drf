function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getToken('csrftoken')

var list_snapshot = [];


displayCart();
displayBurgers();

function displayBurgers() {
  var wrapper = document.getElementById("burger-wrapper");

  fetch("/api/burger-list/")
    .then((resp) => resp.json())
    .then(function (data) {
      //console.log("Burgers:", data);

      var burger = data;
      for (var i in burger) {
        var item = `
                  <div class="col-sm-4">
                      <div class="card mb-4 shadow-sm">
                          <img class="bd-placeholder-img card-img-top" width="100%" height="225" src="${burger[i].image}" alt="">
                          <div class="card-body">
                              <div class="d-flex justify-content-between align-items-center py-3">
                                  <h4 class="my-0 font-weight-normal">${burger[i].name}</h4>
                                  <big class="text-muted">$${burger[i].price}</big>
                              </div>  
                              <p class="card-text">${burger[i].description}</p>
                              <div class="d-flex justify-content-between align-items-center">
                                  <button data-product="${burger[i].id}" data-action="add" class="btn btn-block btn-outline-secondary add-btn update-cart">Add to cart</button>
                              </div>
                          </div>
                      </div>
                  </div>
                  
                  `;
        wrapper.innerHTML += item;
      }

      for (var i in burger) {
        var addBtn = document.getElementsByClassName("add-btn")[i];
        //console.log(addBtn)

        addBtn.addEventListener(
          "click",
          (function (burger) {
            return function () {
              addBurger(burger);
            };
          })(burger[i])
        );
      }
      
    });
}

function displayCart() {
  var wrapper = document.getElementById("cart-wrapper");

  fetch("/api/order-burger-list/")
    .then((resp) => {
      //console.log(resp)
      return resp.json()
    })
    .then(function (data) {
    //console.log("Cart:", data);
    var burger = data;
    if (burger != '') {

      try {
        document.getElementById('empty-cart').remove();
      } catch (err) {}

      for (var i in burger) {
        
        try {
          document.getElementById(`data-row-${i}`).remove();
        } catch (err) {}

        var item = `
                <div id="data-row-${i}">
                  <div class="d-flex justify-content-between align-items-center py-2">
                    <span class="">${burger[i].get_burger}</span>
                    <span class="">$${burger[i].get_total}</span>
                  </div>  
                  <div class="d-flex justify-content-between align-items-center py-1">
                    <button type="button" data-product="${burger[i].id}" data-action="remove" class="remove chg-quantity update-cart close" aria-label="Close">
                      <span aria-hidden="true">&laquo;</span>
                    </button>
                    <span class="">${burger[i].quantity}</span>
                    <button type="button" data-product="${burger[i].id}" data-action="add" class="add chg-quantity update-cart close" aria-label="Close">
                      <span aria-hidden="true">&raquo;</span>
                    </button>
                    <button type="button" data-product="${burger[i].id}" data-action="delete" class="update-cart close delete-btn" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                </div>
                `;
        wrapper.innerHTML += item;
      }

      if (list_snapshot.length > burger.length) {
        for (var i = burger.length; i < list_snapshot.length; i++) {
          //console.log('Delete Duplicates',i)
          document.getElementById(`data-row-${i}`).remove();
        }
      }

      list_snapshot = burger;
      

      for (var i in burger) {
        var deleteBtn = document.getElementsByClassName("delete-btn")[i];
        var addQty = document.getElementsByClassName("add")[i];
        var removeQty = document.getElementsByClassName("remove")[i];
        
        addQty.addEventListener(
          "click",
          (function (burger) {
            return function () {
              var action = this.dataset.action
              console.log('Action:', action)
              //console.log('addQty', burger)
              updateUserOrder(burger, action);
            };
          })(burger[i])
        );

        removeQty.addEventListener(
          "click",
          (function (burger) {
            return function () {
              var action = this.dataset.action
              console.log('Action:', action)
              //console.log('addQty', burger)
              updateUserOrder(burger, action);
            };
          })(burger[i])
        );

        deleteBtn.addEventListener(
          "click",
          (function (burger) {
            return function () {
              //console.log('deleteBtn', burger)
              deleteBurger(burger);
            };
          })(burger[i])
        );

      }

    }else{
      var item = `
                  <div class="d-flex justify-content-center align-items-center py-2">
                    <span id="empty-cart">Empty</span>
                  </div>  
                `;
        wrapper.innerHTML = item;
    }
  });
}




function updateUserOrder(burger, action) {
  
  fetch(`/api/update-order-burger/${burger.id}/`)
  .then((resp) => {
    return resp.json()
  })
  .then((data) => {
    //console.log(data)
    var burgerId = data.burger;
    var quantity = data.quantity;

    if (action == 'add') {
      quantity += 1
    } else if (action == 'remove') {
      quantity -= 1
      if (quantity < 1) {
        console.log('Quantity should be 1')
        quantity = 1;
      }
    }

    fetch("/api/order-list/")
    .then((resp) => {
      return resp.json()
    })
    .then((data) => {

      var order = data.slice(-1)[0];
      //console.log(order)
      
      fetch(`/api/update-order-burger/${burger.id}/`, {
        method: "PUT",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          'burger': burgerId,
          'quantity': quantity,
          'order': order.id,
        }),
      }).then((response) => {
        displayCart();
      });
    })
  })

}
  
    
function addBurger(burger) {
  fetch("/api/order-list/")
  .then((resp) => {
    //console.log('resolved',resp)
    //console.log(resp)
    return resp.json()
  })
  .then((data) => {
    //console.log('No loop',data.slice(-1)[0])
    //for (var i in data) 
      var order = data.slice(-1)[0];
      if (order == undefined) {
        alert('You need to log in!')
      } else {
        //console.log(order)
        //return order
        fetch("/api/order-burger-list/", {
          method: "POST",
          headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            'burger': burger.id,
            'quantity': 1,
            'order': order.id,
          }),
        }).then((response) => {
          displayCart();
        });
      }
  }).catch((err) => {
    console.log('rejected', err)
  })
}


function deleteBurger(burger) {
  console.log("delete clicked");
  fetch(`/api/update-order-burger/${burger.id}/`, {
    method: "DELETE",
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  }).then((response) => {
    displayCart();
  });
}