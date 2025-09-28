// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from irob_interfaces:srv/Deactivate.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__STRUCT_HPP_
#define IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__irob_interfaces__srv__Deactivate_Request __attribute__((deprecated))
#else
# define DEPRECATED__irob_interfaces__srv__Deactivate_Request __declspec(deprecated)
#endif

namespace irob_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Deactivate_Request_
{
  using Type = Deactivate_Request_<ContainerAllocator>;

  explicit Deactivate_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit Deactivate_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    irob_interfaces::srv::Deactivate_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const irob_interfaces::srv::Deactivate_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::Deactivate_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::Deactivate_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__irob_interfaces__srv__Deactivate_Request
    std::shared_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__irob_interfaces__srv__Deactivate_Request
    std::shared_ptr<irob_interfaces::srv::Deactivate_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Deactivate_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const Deactivate_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Deactivate_Request_

// alias to use template instance with default allocator
using Deactivate_Request =
  irob_interfaces::srv::Deactivate_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace irob_interfaces


#ifndef _WIN32
# define DEPRECATED__irob_interfaces__srv__Deactivate_Response __attribute__((deprecated))
#else
# define DEPRECATED__irob_interfaces__srv__Deactivate_Response __declspec(deprecated)
#endif

namespace irob_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Deactivate_Response_
{
  using Type = Deactivate_Response_<ContainerAllocator>;

  explicit Deactivate_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit Deactivate_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    irob_interfaces::srv::Deactivate_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const irob_interfaces::srv::Deactivate_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::Deactivate_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::Deactivate_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__irob_interfaces__srv__Deactivate_Response
    std::shared_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__irob_interfaces__srv__Deactivate_Response
    std::shared_ptr<irob_interfaces::srv::Deactivate_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Deactivate_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const Deactivate_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Deactivate_Response_

// alias to use template instance with default allocator
using Deactivate_Response =
  irob_interfaces::srv::Deactivate_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace irob_interfaces

namespace irob_interfaces
{

namespace srv
{

struct Deactivate
{
  using Request = irob_interfaces::srv::Deactivate_Request;
  using Response = irob_interfaces::srv::Deactivate_Response;
};

}  // namespace srv

}  // namespace irob_interfaces

#endif  // IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__STRUCT_HPP_
