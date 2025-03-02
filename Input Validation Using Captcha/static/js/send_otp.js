$(document).ready(function() {
    // Function to send OTP to the user's phone number
    $('#sendOTP').on('click', function() {
        var phoneNumber = $('#phoneNumber').val();
        
        if (phoneNumber) {
            // You should make an AJAX request to your backend server to send the OTP.
            // Your backend should generate a unique 4-digit OTP and send it to the provided phone number.
            $.ajax({
                type: 'POST',
                url: '/your-backend-endpoint-for-sending-otp',
                data: { phoneNumber: phoneNumber },
                success: function(response) {
                    // Handle the response from your backend, which could be a success message or an error.
                    $('#otpStatus').text(response);
                },
                error: function(error) {
                    // Handle errors, e.g., if the phone number is invalid or the OTP could not be sent.
                    $('#otpStatus').text('Error: ' + error.responseText);
                }
            });
        } else {
            $('#otpStatus').text('Please enter a valid phone number.');
        }
    });
    
    // Function to verify the OTP
    $('#verifyOTP').on('click', function() {
        var otp = $('#otpInput').val();
        
        if (otp) {
            // You should make an AJAX request to your backend to verify the OTP.
            $.ajax({
                type: 'POST',
                url: '/your-backend-endpoint-for-verifying-otp',
                data: { otp: otp },
                success: function(response) {
                    // Handle the response from your backend, which could indicate successful verification or an error.
                    $('#otpStatus').text(response);
                },
                error: function(error) {
                    // Handle errors, e.g., if the OTP is invalid or has expired.
                    $('#otpStatus').text('Error: ' + error.responseText);
                }
            });
        } else {
            $('#otpStatus').text('Please enter the OTP you received.');
        }
    });
});
