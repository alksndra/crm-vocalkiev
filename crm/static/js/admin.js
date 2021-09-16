if (!$) {
    $ = django.jQuery;
}

$(document).ready(function() {
    $("select[name='client_subscription']").change(function() {
        let client_subscription = $('select[name="client_subscription"] option:selected').text()
        $("input[name='amount']").val(1 * client_subscription.split('-')[1].split('-')[0]);
    });
});
