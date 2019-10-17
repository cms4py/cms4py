const Dialog = {
    showLoading(msg) {
        return $(`<div class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
      <div class="modal-body">
        <p>${msg}</p>
      </div>
    </div>
  </div>
</div>`).modal({
            keyboard: false,
            backdrop: "static",
        }).appendTo(document.body).on("hide.bs.modal", function (e) {
            $(this).remove();
        });
    },

    showMessageDialog(msg, title = "", closeCallback) {
        return $(`<div class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">${title}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        ${msg}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-danger" data-dismiss="modal">OK</button>
      </div>
    </div>
  </div>
</div>`).modal({
            keyboard: true,
            backdrop: true,
        }).appendTo(document.body).on("hide.bs.modal", function (e) {
            $(this).remove();
            if (closeCallback) {
                closeCallback();
            }
        });
    }
};

export default Dialog;