// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from irob_interfaces:srv/Deactivate.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__TRAITS_HPP_
#define IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__TRAITS_HPP_

#include "irob_interfaces/srv/detail/deactivate__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<irob_interfaces::srv::Deactivate_Request>()
{
  return "irob_interfaces::srv::Deactivate_Request";
}

template<>
inline const char * name<irob_interfaces::srv::Deactivate_Request>()
{
  return "irob_interfaces/srv/Deactivate_Request";
}

template<>
struct has_fixed_size<irob_interfaces::srv::Deactivate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<irob_interfaces::srv::Deactivate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<irob_interfaces::srv::Deactivate_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<irob_interfaces::srv::Deactivate_Response>()
{
  return "irob_interfaces::srv::Deactivate_Response";
}

template<>
inline const char * name<irob_interfaces::srv::Deactivate_Response>()
{
  return "irob_interfaces/srv/Deactivate_Response";
}

template<>
struct has_fixed_size<irob_interfaces::srv::Deactivate_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<irob_interfaces::srv::Deactivate_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<irob_interfaces::srv::Deactivate_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<irob_interfaces::srv::Deactivate>()
{
  return "irob_interfaces::srv::Deactivate";
}

template<>
inline const char * name<irob_interfaces::srv::Deactivate>()
{
  return "irob_interfaces/srv/Deactivate";
}

template<>
struct has_fixed_size<irob_interfaces::srv::Deactivate>
  : std::integral_constant<
    bool,
    has_fixed_size<irob_interfaces::srv::Deactivate_Request>::value &&
    has_fixed_size<irob_interfaces::srv::Deactivate_Response>::value
  >
{
};

template<>
struct has_bounded_size<irob_interfaces::srv::Deactivate>
  : std::integral_constant<
    bool,
    has_bounded_size<irob_interfaces::srv::Deactivate_Request>::value &&
    has_bounded_size<irob_interfaces::srv::Deactivate_Response>::value
  >
{
};

template<>
struct is_service<irob_interfaces::srv::Deactivate>
  : std::true_type
{
};

template<>
struct is_service_request<irob_interfaces::srv::Deactivate_Request>
  : std::true_type
{
};

template<>
struct is_service_response<irob_interfaces::srv::Deactivate_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__TRAITS_HPP_
