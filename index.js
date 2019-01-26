//noinspection JSUnresolvedFunction
var homepage = angular.module('homePage' , ["ngRoute"]);
homepage.controller('mainMenu' , function($scope) {
    $scope.menuItems = [ {
        item : 'Gallery', link : 'gallery.html'
    } , {
        item : 'Contact Us', link : 'contact.html'
    }];

    
});

